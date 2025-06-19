<script setup>
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { getLogin } from "../api/user";
import { ref } from "vue";

const pop = popStore();
const user = userStore();
// 账号
const formData = ref({
  username: "",
  password: "",
});

// 登录按钮
const submitForm = async () => {
  const res = await getLogin(formData.value);
  if (res) {
    localStorage.setItem("token", "Bearer " + res);
    user.getLoginInfo();
    user.changeUsername(formData.value.username);
    pop.changeLoginPop();
  }
};
</script>

<template>
  <el-dialog v-model="pop.loginPop" title="登录" width="500">
    <div class="form-out">
      <el-form name="register" @submit.native.prevent="submitForm">
        <!-- 账号 -->
        <el-form-item name="account">
          <el-input placeholder="请输入账号" v-model="formData.username" />
        </el-form-item>
        <!-- 密码 -->
        <el-form-item name="password">
          <el-input
            type="password"
            placeholder="请输入密码"
            v-model="formData.password"
          />
        </el-form-item>
        <!-- 登录 -->
        <el-form-item>
          <el-button type="primary" class="login-button" @click="submitForm">
            <span>立即登录</span>
          </el-button>
        </el-form-item>
        <!-- 跳转注册 -->
        <div class="register-out">
          <span>没有账号?</span>
          <span
            class="register-button"
            @click="
              () => {
                pop.changeLoginPop();
                pop.changeRegisterPop();
              }
            "
            >立即注册</span
          >
        </div>
      </el-form>
    </div>
  </el-dialog>
</template>

<style lang="less" scoped>
::v-deep(.el-form) {
  width: 50%;
}
.register-out {
  margin-left: 50px;
  .register-button:hover {
    color: #409eff;
  }
}
.form-out {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  .login-button {
    color: #fff;
    border-radius: 10px;
    width: 100%;
  }
}
</style>
