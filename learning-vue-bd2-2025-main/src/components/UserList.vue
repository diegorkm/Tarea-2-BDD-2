<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import type { User } from '@/interfaces'
import { fetchUsers, createUser } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const users: Ref<User[]> = ref([])
const loading = ref(false)
const search = ref('')

const headers = [
  { title: 'ID', key: 'id', sortable: true },
  { title: 'Usuario', key: 'username', sortable: true },
  { title: 'Nombre Completo', key: 'fullname', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false },
]

// --- NUEVO: estado para crear usuario ---
const dialogCreate = ref(false)
const newUser = ref({
  username: '',
  fullname: '',
  password: '',
})

async function getUsers() {
  loading.value = true
  try {
    users.value = await fetchUsers()
  } catch (error) {
    console.error('Error al cargar usuarios:', error)
  } finally {
    loading.value = false
  }
}

async function goToEditUser(userId: number) {
  await router.push({ name: 'userEdit', params: { id: userId } })
}

// --- NUEVO: abrir el diálogo de creación ---
function openCreateDialog() {
  newUser.value = {
    username: '',
    fullname: '',
    password: '',
  }
  dialogCreate.value = true
}

// --- NUEVO: enviar el formulario y crear usuario ---
async function handleCreateUser() {
  try {
    await createUser(newUser.value)
    dialogCreate.value = false
    await getUsers()
  } catch (error) {
    console.error('Error al crear usuario:', error)
    // aquí podrías mostrar un snackbar/mensaje si quieres
  }
}

onMounted(() => {
  getUsers()
})
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card elevation="4">
          <v-card-title class="d-flex align-center pa-6">
            <v-icon icon="mdi-account-multiple" size="large" class="mr-3"></v-icon>
            <span class="text-h4">Lista de Usuarios</span>
            <v-spacer></v-spacer>

            <!-- NUEVO: botón Agregar usuario -->
            <v-btn
              color="primary"
              class="mr-2"
              prepend-icon="mdi-account-plus"
              @click="openCreateDialog"
            >
              Agregar usuario
            </v-btn>

            <v-btn
              color="primary"
              prepend-icon="mdi-refresh"
              @click="getUsers"
              :loading="loading"
            >
              Recargar
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Buscar usuarios"
              variant="outlined"
              hide-details
              class="mb-4"
            ></v-text-field>

            <v-data-table
              :headers="headers"
              :items="users"
              :search="search"
              :loading="loading"
              loading-text="Cargando usuarios..."
              no-data-text="No hay datos de usuarios cargados."
              :items-per-page="10"
              class="elevation-1"
            >
              <template #item.username="{ item }">
                <v-chip color="primary" variant="tonal">
                  <v-icon icon="mdi-account" start></v-icon>
                  {{ item.username }}
                </v-chip>
              </template>

              <template #item.fullname="{ item }">
                <span class="font-weight-medium">{{ item.fullname }}</span>
              </template>

              <template #item.actions="{ item }">
                <v-btn
                  color="info"
                  variant="tonal"
                  size="small"
                  prepend-icon="mdi-pencil"
                  @click="goToEditUser(item.id)"
                >
                  Editar
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialogCreate" max-width="500" persistent>
        <v-card elevation="8" class="pa-2">
            <v-card-title class="d-flex align-center justify-center text-h6">
                <v-icon icon="mdi-account-plus" color="primary" class="mr-2" />
                Agregar Usuario
            </v-card-title>
            <v-divider class="mb-4" />
             <v-card-text>
                <v-text-field
                v-model="newUser.username"
                label="Usuario"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                color="primary"
                density="comfortable"
                hide-details="auto"
                required
                />
                <v-text-field
                v-model="newUser.fullname"
                label="Nombre completo"
                prepend-inner-icon="mdi-account-badge"
                variant="outlined"
                color="primary"
                density="comfortable"
                hide-details="auto"
                class="mt-3"
                required
                />
                <v-text-field
                v-model="newUser.password"
                label="Contraseña"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                color="primary"
                density="comfortable"
                hide-details="auto"
                class="mt-3"
                required
                />
            </v-card-text>
            <v-card-actions class="justify-end">
                <v-btn variant="text" color="grey-darken-1" @click="dialogCreate = false">
                    Cancelar
                </v-btn>
                <v-btn
                color="primary"
                variant="elevated"
                prepend-icon="mdi-content-save"
                @click="handleCreateUser"
                >
                Guardar
            </v-btn>
        </v-card-actions>
    </v-card>
    </v-dialog>

  </v-container>
</template>

<style scoped></style>
