<template>
  <div class="dashboard-container">
    <component :is='currentRole' />
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import adminDeshboard from "./admin"
import userDeshboard from "./user"

export default {
  name: "Deshboard",
  components: {},
  data() {
    return {
      currentRole: "adminDeshboard"
    }
  },
  computed:{
    ...mapGetters([
      'userinfo'
    ])
  },
  created(){
    if (!this.userinfo.isAdmin){
      this.currentRole = 'userDeshboard'
    }
  }

}
</script>
