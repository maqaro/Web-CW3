﻿<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  <div class="h3">
    {{ title }}
  </div>
  <div class="content">
    <div class="Banner-section blue-color ">
      <div id="banner-image"></div>
      <div id="banner-lower-section" class="hobby-title">
        <h4 class="blue-color">{{ username }}</h4>
        <button id="edit-button" @click="openProfileEditModal"><i class="fa-solid fa-pen"></i> Edit</button>
      </div>
    </div>
    <div class="bottom-section">
      <div>
        <div id="Details_section" class="Table">
          <h4 class="blue-color">Details</h4>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-user"></i></b> : {{ name }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-envelope"></i></b> : {{ email }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-pen-nib"></i></b> : {{ bio }}</div>
          <div class="Details-item"><b class="blue-color"><i class="fa-solid fa-calendar-days"></i></b> : {{ dob }}</div>
        </div>
      </div>
      <div id="Hobbies_section" class="Table full-width-table">
        <div class="hobby-title">
          <h4 class="blue-color">Hobbies</h4>
          <button id="add-button" @click="openHobbiesAddModal"><i class="fa-solid fa-plus"></i> Add</button>
        </div>
        <div class="Table-Row blue-color" v-for="hobby in hobbies" :key="hobby.name">
          {{ hobby.name }}
          <div>
            <button class="btn btn-primary" @click="removeHobby(hobby.name)">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL TEMPLATE FOR PROFILE EDIT -->
  <div class="modal fade" id="ProfileEditModal" aria-labelledby="ProfileEditModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Edit Profile</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div>
            <label for="username">Username</label>
            <input class="form-control" type="text" id="username" v-model="username" />
          </div>
          <div>
            <label for="email">Email</label>
            <input class="form-control" type="email" id="email" v-model="email" />
          </div>
          <div>
            <label for="bio">Bio</label>
            <textarea class="form-control" id="bio" v-model="bio"></textarea>
          </div>
          <div>
            <label for="dob">Date of Birth</label>
            <input class="form-control" type="date" id="dob" v-model="dob" />
          </div>
          <div>
            <label for="password">Enter New Password</label>
            <input class="form-control" type="password" id="password" v-model="password" />
          </div>
          <div>
            <label for="confirm-password">Confirm New Password</label>
            <input class="form-control" type="password" id="confirm-password" v-model="confirmPassword" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" id="save-button" class="btn btn-primary" @click="saveProfileEditModal">Save changes</button>
          <button type="button" class="btn btn-secondary" @click="closeProfileEditModal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL TEMPLATE FOR HOBBY ADD -->
  <div class="modal fade" id="HobbyAddModal" aria-labelledby="HobbyAddModal" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1>Add Hobby</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="hobby-name">Please select an existing hobby</label>
            <select id="hobby-select" class="form-control" v-model="selectedHobbyOption">
              <option :id=" hobby_title " :value="hobby_title" v-for="hobby_title in all_hobbies" :key="hobby_title">{{ hobby_title }}</option>
              <option value="Other">New Hobby</option>
            </select>
            
            <div v-if="selectedHobbyOption === 'Other'">
              <p class="mt-3 mb-2">Enter new hobby here</p>
              <input 
                type="text" 
                id="hobby-name" 
                class="form-control" 
                v-model="newHobby"
                :class="{'is-invalid': addHobbyError}"
              />
              <div class="invalid-feedback" v-if="addHobbyError">
                {{ addHobbyError }}
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button 
            id="save-button"
            type="button" 
            class="btn btn-primary" 
            @click="saveAddHobbyModal"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Adding...' : 'Add Hobby' }}
          </button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from "vue";
import 'bootstrap';
import * as bootstrap from 'bootstrap';
import { getCsrfToken } from '../utils/auth.ts';

interface Hobby {
  name: string;
}

export default defineComponent({
  inheritAttrs: false,
  setup() {
    const title = ref("Profile");
    const username = ref("");
    const name = ref("");
    const email = ref("");
    const bio = ref("");
    const dob = ref("");
    const hobbies = ref<Hobby[]>([]);
    const selectedHobby = ref("");
    const newHobby = ref("");
    const addHobbyError = ref("");
    const isSubmitting = ref(false);
    var temp_username = "";
    var temp_email = "";
    var temp_bio = "";
    var temp_dob = "";
    const all_hobbies = ref([]);
    const selectedHobbyOption = ref("");
    const password = ref("");
    const confirmPassword = ref("");


    watch(selectedHobbyOption, (newValue) => {
      if (newValue === 'Other') {
        newHobby.value = "";
      } else {
        newHobby.value = newValue;
      }
    });

    const fetchUserProfile = async () => {
      try {
        const response = await fetch('/api/profile/');
        if (!response.ok) {
          throw new Error('Failed to fetch user profile');
        }
        const data = await response.json();
        username.value = data.username;
        name.value  = data.first_name + " " + data.last_name;
        email.value = data.email;
        bio.value = data.bio;
        dob.value = data.date_of_birth;
        hobbies.value = data.hobbies.map((hobby: string) => ({ name: hobby }));
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };

    const fetchHobbies = async () => {
      try {
        const response = await fetch('/api/get_all_hobbies/');
        if (!response.ok) {
          throw new Error('Failed to fetch all hobbies');
        }
        const data = await response.json();
        all_hobbies.value = data.hobbies;
      } catch (error) {
        console.error('Error fetching Hobbies:', error);
      }
    }
    const closeProfileEditModal = () => {
      username.value = temp_username;
      email.value = temp_email;
      bio.value = temp_bio;
      dob.value = temp_dob;
      temp_username = "";
      temp_email = "";
      temp_bio = "";
      temp_dob = "";
      const modalElement = document.getElementById('ProfileEditModal');
      if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal?.hide();
      }
    };
    
    const openProfileEditModal = () => {
      temp_username = username.value;
      temp_email = email.value;
      temp_bio = bio.value;
      temp_dob = dob.value;
      const modalElement = document.getElementById('ProfileEditModal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    };
    const saveProfileEditModal = async () => {
      try {
        const csrfToken = await getCsrfToken();
        const modalElement = document.getElementById('ProfileEditModal');
        const modal = modalElement ? bootstrap.Modal.getInstance(modalElement) : null;

        if (password.value !== confirmPassword.value) {
          alert("Passwords do not match. Please try again.");
          return;
        }

        const response = await fetch('/api/update-profile/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include',
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            bio: bio.value,
            dob: dob.value,
            password: password.value,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to update profile');
        }

        const data = await response.json();
        username.value = data.profile.username;
        email.value = data.profile.email;
        bio.value = data.profile.bio;
        dob.value = data.profile.date_of_birth;

        // Clear password fields after successful update
        password.value = '';
        confirmPassword.value = '';

        modal?.hide();
        
      } catch (error: any) {
        alert(`Failed to save profile: ${error.message}`);
      }
    };

    const openEditHobbyModal = (hobby: string) => {
      selectedHobby.value = hobby;
      const modalElement = document.getElementById('HobbyEditModal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    };

    const saveEditHobbyModal = () => {
      
      const modalElement = document.getElementById('HobbyEditModal');
      if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal?.hide();
      }
    };

    const openHobbiesAddModal = () => {
      fetchHobbies();
      const modalElement = document.getElementById('HobbyAddModal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    };
    const saveAddHobbyModal = async () => {
      if (!newHobby.value.trim()) {
        addHobbyError.value = "Hobby name cannot be empty";
        return;
      }

      if (hobbies.value.some(hobby => hobby.name === newHobby.value.trim())) {
        addHobbyError.value = "You already have this hobby";
        return;
      }

      isSubmitting.value = true;
      addHobbyError.value = "";

      try {
        const csrfToken = await getCsrfToken();
        const response = await fetch('/api/add-hobby/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({
            name: newHobby.value.trim()
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to add hobby');
        }

        hobbies.value.push({ name: newHobby.value.trim() });
        newHobby.value = "";
        
        const modalElement = document.getElementById('HobbyAddModal');
        if (modalElement) {
          const modal = bootstrap.Modal.getInstance(modalElement);
          modal?.hide();
        }

      } catch (error: any) {
        addHobbyError.value = error.message;
      } finally {
        isSubmitting.value = false;
      }
    };

    const removeHobby = async (hobby: string) => {
      try {
        const csrfToken = await getCsrfToken();
        const response = await fetch('/api/remove-hobby/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({ name: hobby }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to remove hobby');
        }

        hobbies.value = hobbies.value.filter(h => h.name !== hobby);
      } catch (error: any) {
        alert(`Failed to remove hobby: ${error.message}`);
      }
    };

    onMounted(() => {
      fetchUserProfile();
    });

    return {
      title,
      username,
      name,
      email,
      bio,
      dob,
      hobbies,
      selectedHobby,
      newHobby,
      addHobbyError,
      isSubmitting,
      all_hobbies,
      openProfileEditModal,
      saveProfileEditModal,
      openEditHobbyModal,
      saveEditHobbyModal,
      openHobbiesAddModal,
      saveAddHobbyModal,
      closeProfileEditModal,
      fetchHobbies,
      selectedHobbyOption,
      password,
      confirmPassword,
      removeHobby
    };
  }
});
</script>

<style scoped>
.full-width-table
{
  width: 100%;
}
.hobby-title
{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.Banner-section
{
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 1rem;
}
.bottom-section
{
  display: grid;
  grid-template-columns: 35% 1% 64%;
  grid-template-areas: 
  'Details_section . Hobbies_section'
  ;
  max-width: 100%;
}
.Table
{
  display: flex;
  flex-direction: column;
  border-radius: 0.5rem;
  background-color: white;
  padding: 1rem;
  
}
.Table-Row
{
  display: flex;
  flex-direction: row;
  padding: 1rem;
  margin-left: 1rem;
  margin-right: 1rem;
  justify-content: space-between;
  border-bottom: black 1pt solid;
}
.content
{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  background-color: #e5e5e5;
  border-radius: 0.5rem;
  padding: 1rem;
}
#Hobbies_section
{
  grid-area: Hobbies_section;
}
#Details_section
{
  grid-area: Details_section;
}
.Details-item
{
  padding: 1rem;
  border-bottom: 1pt solid #0a53be;
  margin-left: 1rem;
  margin-right: 1rem;
  white-space: nowrap;
  overflow: hidden;
  word-break: break-word;
  text-overflow: ellipsis;
}
h4
{
  padding: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  word-break: break-word;
  text-overflow: ellipsis;
}
.blue-color
{
  color: #0a53be;
}
#banner-image
{
  width: 100%;
  height: 10rem;
  border: solid 1pt #0a53be;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}
#add-button, #edit-button
{
  background-color: #0a53be;
  border-color: #0a53be;
  border-radius: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  color: white;
}
#banner-lower-section
{
  padding: 0.5rem;
  padding-right: 1rem;
}
</style>