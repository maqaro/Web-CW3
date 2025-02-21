<template>
    <main class="container pt-4">
        <nav class="nav-container">
          <div class="nav-element-container">
            <router-link
                id="profile-link"
                class="nav-link"
                :to="{name: 'Profile'}"
            >
              Profile
            </router-link>

            <router-link
                id="hobbies-link"
                class="nav-link"
                :to="{name: 'Hobbies Page'}"
            >
              Hobbies
            </router-link>
            <router-link
                id="friends-link"
                class="nav-link"
                :to="{name: 'Friends Page'}"
            >
              Friends
            </router-link>
          </div>
          <div class="user-info">
              <button @click="handleLogout" class="btn-logout">Logout</button>
          </div>
        </nav>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView, useRouter } from "vue-router";
import { useUserStore } from './stores/userStore';

export default defineComponent({
    components: { RouterView },
    setup() {
        const userStore = useUserStore();
        const router = useRouter();
        
        const handleLogout = async () => {
            try {
                const csrfToken = getCookie('csrftoken') || '';
                const response = await fetch('/api/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    credentials: 'include',
                });
                
                const data = await response.json();
                if (data.success) {
                    userStore.clearUser();
                    window.location.href = data.redirect_url;
                }
            } catch (err) {
                console.error('Logout error:', err);
            }
        };

        function getCookie(name: string): string | null {
            let cookieValue: string | null = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        return {
            userStore,
            router,
            handleLogout,
        };
    }
});
</script>

<style>
:root{
    --primary-color: #2D68FE;
    --primary-color-light: #2d68fe5d;
}


/* Additional custom styles */
.nav-link {
    text-decoration: none;
    padding: 0.5rem 1rem;
    margin-right: 1rem;
    font-weight: 900 !important;
}

.nav-link:hover {
    color: var(--primary-color) !important;
}

.router-link-active {
    color: var(--primary-color) !important;
    background-color: var(--primary-color-light) !important;
    font-weight: bold;
}

nav {
    margin-bottom: 2rem;
    padding: 1rem;
    background: #fff;
    border-radius: 4px;;
    display: flex;
    flex-direction: row;
    margin-right: 1rem;
}

.container {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    max-width: 1140px;
}

.pt-4 {
    padding-top: 1.5rem;
}

.user-info {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
}

.btn-logout {
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    background-color: #dc3545;
    color: white;
    border: none;
    cursor: pointer;
}
.nav-container
{
  justify-content: space-between;
}
.nav-element-container
{
  display: flex;
  flex-direction: row;
}
.btn-logout:hover {
    background-color: #c82333;
}
</style>
