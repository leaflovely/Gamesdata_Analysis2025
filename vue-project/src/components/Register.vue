<script setup>
import { popStore } from "../store/pop";
import { getRegister } from "../api/user";
import { ref } from "vue";

const pop = popStore();
// 账号
const formData = ref({
  username: "",
  password: "",
});

// 注册按钮
const submitForm = async () => {
  const res = await getRegister(formData.value);
  if (res === "注册成功") {
    pop.changeRegisterPop();
    pop.changeLoginPop();
  } else {
    console.log(res);
  }
};
</script>

<template>
  <el-dialog v-model="pop.registerPop" title="注册" width="500">
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
        <!-- 注册 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" class="login-button">
            <span>立即注册</span>
          </el-button>
        </el-form-item>
        <!-- 跳转登录 -->
        <div class="register-out">
          <span>已有账号?</span>
          <span
            class="register-button"
            @click="
              () => {
                pop.changeRegisterPop();
                pop.changeLoginPop();
              }
            "
            >立即登录</span
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
