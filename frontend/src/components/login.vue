<template>
  <el-tabs type="border-card" class="border-card">
    <el-tab-pane label="登录">
      <el-form v-model="loginInfo">
        <el-form-item label="用户名">
          <el-input v-model="loginInfo.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginInfo.password" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="login">登录</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
    <el-tab-pane label="注册">
      <el-form v-model="signUpInfo">
        <el-form-item label="用户名">
          <el-input v-model="signUpInfo.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="signUpInfo.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="再次输入">
          <el-input v-model="checkpwd" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="signup">注册</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import api from "../api/api";

export default {
  name: "login",
  data() {
    return {
      loginInfo: {},
      signUpInfo: {},
      checkpwd: null
    };
  },
  methods: {
    async login() {
      if (this.loginInfo.username && this.loginInfo.password) {
        let res = await api.login(this.loginInfo);
        if (res.code === 1) {
          this.loginInfo = {};
          this.$emit("updateInput", true);
        } else {
          alert(res.message);
        }
      } else {
        alert("你漏填了东西");
      }
    },
    async signup() {
      if (this.signUpInfo.username && this.signUpInfo.password && this.checkpwd) {
        if (this.signUpInfo.password === this.checkpwd) {
          let res = await api.register(this.signUpInfo);
          console.log({ res });
          if (res.code === 1) {
            this.$emit("updateInput", true);
          } else {
            alert(res.message);
          }
        } else {
          alert("两次输入密码不一致");
        }
      } else {
        alert("你漏填了东西");
      }
    }
  }
};
</script>

<style scoped>
.border-card {
  width: 60%;
  margin: 5% auto;
}
</style>