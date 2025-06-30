<script setup>
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { getLogin } from "../api/user";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const pop = popStore();
const user = userStore();
const route = useRoute();
const router = useRouter();

// 登录表单数据
const formData = ref({
  username: "",
  password: "",
});

// 记住账号状态
const rememberAccount = ref(false);

// 表单验证规则
const loginRules = ref({
  username: [
    { required: true, message: "请输入账号", trigger: "blur" }
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, message: "密码长度至少为6位", trigger: "blur" }
  ]
});

// 表单引用
const loginFormRef = ref(null);

// 登录按钮加载状态
const isLoading = ref(false);

// 登录处理
const submitForm = async () => {
  // 表单验证
  loginFormRef.value.validate((valid) => {
    if (!valid) return false;
    
    isLoading.value = true;
    // 登录请求
    loginAction(formData.value);
  });
};

// 登录处理
const loginAction = async (loginData) => {
  try {
    const res = await getLogin(loginData);
    if (res) {
      // 存储令牌
      localStorage.setItem("token", "Bearer " + res);
      
      // 存储账号（如果勾选记住账号）
      if (rememberAccount.value) {
        localStorage.setItem("rememberedUsername", formData.value.username);
      }
      
      // 更新用户信息
      await user.getLoginInfo();
      user.changeUsername(formData.value.username);
      
      // 关闭弹窗
      pop.changeLoginPop();
      
      // 登录成功提示
      pop.showMessage("登录成功", "success");
      
      // 跳转回原页面或首页
      const redirect = route.query.redirect || "/";
      router.push(redirect);
    }
  } catch (error) {
    console.error("登录失败", error);
    pop.showMessage("登录失败，请检查账号密码", "error");
  } finally {
    isLoading.value = false;
  }
};

// 自动填充记住的账号
onMounted(() => {
  const rememberedUsername = localStorage.getItem("rememberedUsername");
  if (rememberedUsername) {
    formData.value.username = rememberedUsername;
    rememberAccount.value = true;
  }
});
</script>

<template>
  <el-dialog 
    v-model="pop.loginPop" 
    width="480px" 
    class="custom-login-dialog"
    :before-close="pop.changeLoginPop"
  >
    <template #header>
      <div class="dialog-header">
        <div class="dialog-title">系统登录</div>
        <div class="close-btn" @click="pop.changeLoginPop">
          <i class="el-icon-close"></i>
        </div>
      </div>
    </template>
    
    <div class="login-content">
      <!-- 品牌标识区域 -->
      <div class="logo-area">
        <div class="logo-icon">
          <img src="/src/assets/logo.png" alt="logo" class="system-logo" />
          <i class="el-icon-user"></i>
        </div>
        <h3 class="logo-title">欢迎登录</h3>
        <p class="logo-subtitle">游戏推荐系统入口</p>
      </div>
      
      <!-- 登录表单 -->
      <el-form 
        ref="loginFormRef" 
        :model="formData" 
        :rules="loginRules"
        class="login-form"
        label-width="0"
      >
        <!-- 账号 -->
        <el-form-item prop="username">
          <el-input 
            placeholder="请输入账号" 
            v-model="formData.username"
            prefix-icon="el-icon-user"
            :class="{ 'input-focus': formData.username }"
          />
        </el-form-item>
        
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input 
            type="password" 
            placeholder="请输入密码" 
            v-model="formData.password"
            prefix-icon="el-icon-lock"
            show-password
            :class="{ 'input-focus': formData.password }"
          />
        </el-form-item>
        
        <!-- 记住账号 -->
        <el-form-item class="remember-me">
          <el-checkbox v-model="rememberAccount">记住账号</el-checkbox>
          <span class="forgot-password">忘记密码?</span>
        </el-form-item>
        
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            @click="submitForm"
            :loading="isLoading"
          >
            <span v-if="!isLoading">立即登录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 跳转注册 -->
      <div class="register-area">
        <span>没有账号?</span>
        <span 
          class="register-link"
          @click="() => { pop.changeLoginPop(); pop.changeRegisterPop(); }"
        >立即注册</span>
      </div>
    </div>
  </el-dialog>
</template>

<style lang="less" scoped>
/* 基础变量定义 */
@primary-color: #165cff96;       // 深蓝色主色调
@primary-light: #4080FF;      // 浅蓝色
@primary-dark: #0E42D2;       // 深暗色
@text-color: #333333;         // 文本颜色
@text-secondary: #666666;     // 次要文本颜色
@bg-color: #FFFFFF;           // 背景颜色
@border-radius: 16px;         // 圆角大小
@box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); // 阴影

/* 对话框样式 */
.custom-login-dialog {
  .el-dialog__header {
    padding: 24px 30px 0;
    border-bottom: none;
  }
  
  .el-dialog__body {
    padding: 0;
  }
}

/* 头部样式 */
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  
  .dialog-title {
    font-size: 22px;
    font-weight: 600;
    color: @text-color;
    margin: 0;
  }
  
  .close-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: @text-secondary;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      background-color: rgba(0, 0, 0, 0.05);
      color: @primary-color;
    }
  }
}

/* 登录内容区 */
.login-content {
  padding: 30px;
  position: relative;
}

/* 品牌标识区域 */
.logo-area {
  text-align: center;
  padding-bottom: 30px;
  position: relative;
  
  .logo-icon {
    position: relative;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background-color: @primary-color;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 64px;
    margin-bottom: 15px;
    box-shadow: 0 5px 15px rgba(22, 93, 255, 0.2);
    animation: logo-float-smooth 2.8s cubic-bezier(0.45,0,0.55,1) infinite;
    /* 外部虚化光圈 */
    &::after {
      content: '';
      position: absolute;
      left: 50%;
      top: 50%;
      width: 200px;
      height: 200px;
      border-radius: 50%;
      transform: translate(-50%, -50%);
      background: radial-gradient(circle, rgba(22,93,255,0.18) 0%, rgba(22,93,255,0.08) 60%, rgba(255,255,255,0) 85%);
      z-index: 0;
      pointer-events: none;
      filter: blur(2px);
    }
    
    .system-logo {
      position: absolute;
      left: 50%;
      top: 50%;
      width: 88px;
      height: 88px;
      border-radius: 50%;
      object-fit: cover;
      transform: translate(-50%, -50%);
      z-index: 2;
      background: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    }
    
    i {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
      opacity: 0.18;
      font-size: 76px;
    }
  }
  
  .logo-title {
    font-size: 20px;
    font-weight: 600;
    color: @text-color;
    margin: 0 0 8px;
  }
  
  .logo-subtitle {
    font-size: 14px;
    color: @text-secondary;
    margin: 0;
  }
}

/* 登录表单样式 */
.login-form {
  padding: 0;
  
  .el-form-item {
    margin-bottom: 20px;
    
    &.remember-me {
      margin-top: -10px;
      margin-bottom: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .el-checkbox {
        color: @text-secondary;
        
        .el-checkbox__inner {
          background-color: transparent;
          border-color: #DDDDDD;
          
          &:hover {
            border-color: @primary-light;
          }
          
          &.is-checked {
            background-color: @primary-color;
            border-color: @primary-color;
          }
        }
        
        .el-checkbox__label {
          color: @text-secondary;
        }
      }
      
      .forgot-password {
        color: @text-secondary;
        cursor: pointer;
        font-size: 13px;
        
        &:hover {
          color: @primary-color;
        }
      }
    }
  }
  
  /* 输入框样式 */
  .el-input {
    .el-input__inner {
      height: 50px;
      background-color: #F5F7FA;
      border: 1px solid #E4E7ED;
      border-radius: 8px;
      color: @text-color;
      padding-left: 45px;
      
      &::placeholder {
        color: #909399;
      }
      
      &:focus {
        border-color: @primary-light;
        box-shadow: 0 0 0 2px rgba(64, 128, 255, 0.2);
      }
    }
    
    .el-input__prefix {
      left: 15px;
      
      .el-input__icon {
        color: #C0C4CC;
      }
    }
  }
  
  /* 输入框聚焦效果 */
  .input-focus {
    .el-input__inner {
      border-color: @primary-light;
    }
  }
}

/* 登录按钮样式 */
.login-button {
  width: 100%;
  height: 50px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  background-color: @primary-color;
  border: none;
  transition: all 0.3s ease;
  
  &:hover {
    background-color: @primary-dark;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(22, 93, 255, 0.3);
  }
  
  &:active {
    transform: translateY(0);
  }
}

/* 注册区域样式 */
.register-area {
  text-align: center;
  margin-top: 20px;
  
  span {
    color: @text-secondary;
    font-size: 14px;
    
    &.register-link {
      color: @primary-color;
      cursor: pointer;
      margin-left: 5px;
      text-decoration: none;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
}

/* 动画效果 */
@keyframes logo-float-smooth {
  0% { transform: translateY(0) scale(1); }
  10% { transform: translateY(-7px) scale(1.03); }
  25% { transform: translateY(-12px) scale(1.05); }
  40% { transform: translateY(-7px) scale(1.03); }
  50% { transform: translateY(0) scale(1); }
  60% { transform: translateY(7px) scale(0.97); }
  75% { transform: translateY(12px) scale(0.95); }
  90% { transform: translateY(7px) scale(0.97); }
  100% { transform: translateY(0) scale(1); }
}

/* 响应式设计 */
@media (max-width: 576px) {
  .custom-login-dialog {
    width: 90%;
  }
  
  .login-content {
    padding: 25px;
  }
  
  .logo-area {
    padding-bottom: 25px;
    
    .logo-icon {
      width: 120px;
      height: 120px;
      font-size: 48px;
      
      &::after {
        width: 160px;
        height: 160px;
      }
      
      .system-logo {
        width: 72px;
        height: 72px;
      }
      
      i {
        font-size: 60px;
      }
    }
  }
  
  .login-form {
    .el-form-item {
      margin-bottom: 18px;
    }
  }
}
</style>