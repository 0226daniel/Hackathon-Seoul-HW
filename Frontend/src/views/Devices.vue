<template>
  <div>
    <v-simple-table :height="500">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">ID</th>
            <th class="text-left">lon</th>
            <th class="text-left">lat</th>
            <th class="text-left">created_at</th>
            <th class="text-left">updated_at</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in devices" :key="item.device_id">
            <td>{{ item.device_id }}</td>
            <td>{{ item.lon }}</td>
            <td>{{ item.lat }}</td>
            <td>{{ item.created_at }}</td>
            <td>{{ item.updated_at }}</td>
            <td>
              <v-btn icon @click="deleteDevice(item.device_id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
@Component
export default class Devices extends Vue {
  devices=[];
  mounted() {
    this.loadList();
  }
  loadList() {
    this.$axios.get('/').then((res) => {
      this.devices = res.data;
    }).catch((err) => {});
  }
  deleteDevice(id: string) {
    if (window.confirm('정말 삭제하시겠습니까?')) {
      this.$axios.delete(`/${id}`).then((res) => {
            this.loadList();
          }).catch((err) => {

          });
      }
  }
}
</script>

<style lang="scss">
</style>
