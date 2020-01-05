<template>
  <div>
    <v-simple-table :height="500">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">ID</th>
            <th class="text-left">device_id</th>
            <th class="text-left">created_at</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in events" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.device_id }}</td>
            <td>{{ item.created_at }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
@Component
export default class Events extends Vue {
  events = [];
  mounted() {
    this.loadList();
  }
  loadList() {
    this.$axios.get('/events').then((res) => {
      this.events = res.data;
    }).catch((err) => {});
  }
}
</script>

<style lang="scss">
</style>
