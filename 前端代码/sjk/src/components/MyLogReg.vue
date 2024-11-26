<template>
    <div class="container">
      <!-- 选择页面 -->
      <div v-show="target == 0" class="select_box">
        <div class="head">小小外卖平台</div>
        <div class="options">
          <el-button type="primary" @click="selectRole(0)">用户</el-button>
          <el-button type="primary" @click="selectRole(1)">管理员</el-button>
        </div>
      </div>
  
      <!-- 登录注册页面 -->
      <div v-show="target > 0" class="login_register_box">
        <div class="head">小小外卖平台</div>
        <!-- 登录 -->
        <div v-show="target == 1">
          <el-form
            label-width="0"
            class="login_form"
            :model="login_form"
            :rules="login_rules"
            ref="login_form"
          >
            <!-- 用户名 -->
            <el-form-item prop="userortel">
              <el-input
                v-model="login_form.userortel"
                spellcheck="false"
                placeholder="手机号"
              ></el-input>
            </el-form-item>
            <!-- 密码 -->
            <el-form-item prop="password">
              <el-input
                v-model="login_form.password"
                show-password
                spellcheck="false"
                placeholder="密码"
              ></el-input>
            </el-form-item>
            
            
            <!-- 按钮 -->
            <el-form-item class="btns">
              <el-button type="primary" @click="llogin()">登录</el-button>
            </el-form-item>
          </el-form>
          <div>
            <div class="operate">
              <span id="op1" @click="change(2)">注册</span>
              <span id="op2" @click="change(3)">忘记密码</span>
            </div>
          </div>
        </div>
  
        <!-- 注册表单 -->
        <div class="reg_box" v-show="target == 2">
          <div class="head">小小外卖平台</div>
          <div>
            <el-form class="reg_form" :model="reg_form" :rules="reg_rules" ref="reg_form">
              <!-- 用户名 -->
              <el-form-item prop="username">
                <el-input
                  prefix-icon="iconfont icon-user"
                v-model="reg_form.username"
                spellcheck="false"
                placeholder="用户名"
                ></el-input>
              </el-form-item>
              <!-- 手机号码 -->
              <el-form-item prop="telephone">
                <el-input
                  prefix-icon="iconfont icon-password"
                  v-model="reg_form.telephone"
                  spellcheck="false"
                  placeholder="手机号码"
                ></el-input>
              </el-form-item>
              <!-- 密码 -->
              <el-form-item prop="password">
                <el-input
                  prefix-icon="iconfont icon-password"
                  v-model="reg_form.password"
                  show-password
                  spellcheck="false"
                  placeholder="密码(包含大小写字母、数字，长度在6-12之间)"
                ></el-input>
              </el-form-item>
              <!-- 真实姓名 -->
      <el-form-item prop="real_name">
        <el-input
          v-model="reg_form.real_name"
          spellcheck="false"
          placeholder="真实姓名"
        ></el-input>
      </el-form-item>
      <!-- 年龄 -->
      <el-form-item prop="age">
        <el-input
          v-model="reg_form.age"
          spellcheck="false"
          placeholder="年龄"
        ></el-input>
      </el-form-item>
      <!-- 性别 -->
      <el-form-item prop="sex">
        <el-select v-model="reg_form.sex" placeholder="性别">
          <el-option label="男" value="男"></el-option>
          <el-option label="女" value="女"></el-option>
        </el-select>
      </el-form-item>
      <!-- 邮箱 -->
      <el-form-item prop="mail">
        <el-input
          v-model="reg_form.mail"
          spellcheck="false"
          placeholder="邮箱"
        ></el-input>
      </el-form-item>

              <!-- 按钮 -->
              <el-form-item class="btns">
                <el-button type="primary" @click="zhuce()">注册</el-button>
              </el-form-item>
            </el-form>
            <div>
              <div>
                <span
                  @click="change(1)"
                  style="margin-left:210px;color: #000;opacity: .5;font-weight: 400;font-size: 16px;cursor:pointer;"
                  >登录</span
                >
              </div>
            </div>
          </div>
        </div>
          
        <!-- 找回密码 -->
        <div class="forget_box" v-show="target == 3">
         <div class="head">小小外卖平台</div>
          <div>
            <el-form class="reg_form" :model="findback_form" :rules="findback_rules" ref="findback_form">
              <el-form-item prop="telephone">
                <el-input
                  prefix-icon="iconfont icon-password"
                  v-model="findback_form.telephone"
                  spellcheck="false"
                  placeholder="手机号码"
                ></el-input>
              </el-form-item>
              <!-- 密码 -->
              <el-form-item prop="password">
                <el-input
                  prefix-icon="iconfont icon-password"
                  v-model="findback_form.password"
                  show-password
                  spellcheck="false"
                  placeholder="新密码"
                ></el-input>
              </el-form-item>
  
              <!-- 按钮 -->
              <el-form-item class="btns">
                <el-button type="primary" @click="findback()">确认修改</el-button>
              </el-form-item>
            </el-form>
            <div>
              <div>
                <span
                  @click="change(1)"
                  style="margin-left:207px;color: #000;opacity: .5;font-weight: 500;font-size: 16px;cursor:pointer;"
                  >登录</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
export default {
  name: 'MyLogin',
  data() {
    var checkPassword = (rule, value, cb) => {
      const regPassword = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{6,12}$/;
      if (regPassword.test(value)) {
        return cb();
      }
      cb(new Error('包含大写字母、小写字母、数字，长度在6-12位之间'));
    };
    var checkMobile = (rule, value, cb) => {
      const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
      if (regMobile.test(value)) {
        return cb();
      }
      cb(new Error('手机号码格式不正确'));
    };
    return {
      target: 0, // 初始值设置为0，显示选择页面
      role: 0, // 用于保存用户选择的角色
      login_form: {
        userortel: '',
        password: '',
      },
      reg_form: {
        username: '',
        telephone: '',
        password: '',
        real_name: '',
        age: '',
        sex: '',
        mail: '',
      },
      findback_form: {
        telephone: '',
        password: '',
      },
      login_rules: {
        userortel: [
          { required: true, message: '请输入电话', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' },
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
      reg_rules: {
        username: [{ required: true, message: '请设置用户名', trigger: 'blur' }],
        telephone: [
          { required: true, message: '请绑定手机号', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请设置密码', trigger: 'blur' },
          { validator: checkPassword, trigger: 'blur' },
        ],
        real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
        age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
        sex: [{ required: true, message: '请选择性别', trigger: 'change' }],
        mail: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
      },
      findback_rules: {
        telephone: [
          { required: true, message: '请输入电话', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: checkPassword, trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
  findback() {
    this.$refs.findback_form.validate((valid) => {
      if (!valid) return;
      if (!this.findback_form.password) {
        this.$message({
          message: '新密码不能为空',
          type: 'error',
        });
        return;
      }
      this.$axios
        .post('/api/user/findback', {
          telephone: this.findback_form.telephone,
          password: this.findback_form.password,
        })
        .then((res) => {
          if (res.data.status === 200) {
            this.$message({
              message: '密码修改成功',
              type: 'success',
            });
            this.target = 1; // 找回密码成功后跳转到登录页面
          } else {
            this.$message({
              message: res.data.msg,
              type: 'error',
            });
          }
        })
        .catch((error) => {
          console.error(error);
          this.$message({
            message: '网络故障',
            type: 'error',
          });
        });
    });
  },


    zhuce() {
      this.$refs.reg_form.validate((valid) => {
        if (!valid) return;
        else {
          this.$axios
            .request({
              method: 'POST',
              url: '/api/user/register', // 修正API URL
              data: {
                username: this.reg_form.username,
                telephone: this.reg_form.telephone,
                password: this.reg_form.password,
                real_name: this.reg_form.real_name,
                age: this.reg_form.age,
                sex: this.reg_form.sex,
                mail: this.reg_form.mail,
                role: this.role, // 添加角色信息
              },
            })
            .then((res) => {
              if (res.data.status == 200) {
                this.$message({
                  message: '注册成功',
                  type: 'success',
                });
                this.target = 1; // 注册成功后跳转到登录页面
              } else {
                this.$message({
                  message: res.data.msg,
                  type: 'error',
                });
              }
            })
            .catch((error) => {
              console.error(error);
              this.$message({
                message: '网络故障',
                type: 'error',
              });
            });
        }
      });
    },
    change(id) {
      this.target = id;
    },
    llogin() {
      this.$refs.login_form.validate((valid) => {
        if (!valid) return;
        else this.login();
      });
    },
    async login() {
      this.$axios.post('/api/user/login', { userortel: this.login_form.userortel, password: this.login_form.password, role: this.role }).then((res) => {
        if (res.data.code != 200) {
          return this.$message({
            message: res.data.msg,
            type: 'error ',
          });
        } else {
          this.$message({
            message: '登录成功',
            type: 'success',
          });

          window.localStorage.setItem('token', res.data.token);

          if (res.data.role == 0) this.$router.push('/user');
          else this.$router.push('/manage');
        }
      }).catch(() => {
        this.$message({
          message: '网络故障',
          type: 'error',
        });
      });
    },
    selectRole(role) {
      this.role = role; // 将选择的角色保存到data中
      this.target = 1; // 进入登录页面
    }
  },
};
</script>

<style lang="less" scoped>
.container {
  background-color: #91b4b3;
  height: 100%;
  width: 100%;
}

.head {
  text-align: center;
  height: 50px;
  line-height: 50px;
  font-size: larger;
}

.select_box {
  height: 350px;
  width: 450px;
  background-color:#ffffff;
  border-radius: 3px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.options {
  display: flex;
  justify-content: space-around;
  width: 100%;
  padding: 20px;
}

.login_register_box {
  height: 300px;
  width: 450px;
  background-color: #ffffff;
  border-radius: 3px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.reg_box {
  height: 600px;
  width: 450px;
  background-color: #ffffff;
  border-radius: 3px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.forget_box {
  height: 300px;
  width: 450px;
  background-color: #FFFFFF;
  border-radius: 3px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.input {
  width: 350px;
  height: 50px;
  margin-left: 50px;
}

.el-form-item {
  width: 350px;
  margin-left: 50px;
}

.btns {
  text-align: center;
}

.operate {
  text-align: center;
  color: #000;
  opacity: 0.5;
  font-weight: 400;
  font-size: 16px;
  margin-left: 28px;
}

.el-input__icon {
  font-size: 20px; /* 调整图标大小 */
  color: #ccc; /* 调整图标颜色 */
  cursor: pointer; /* 添加鼠标指针样式，让用户知道可以点击 */
}

#op1 {
  padding-left: 15px;
  padding-right: 30px;
  border-right: 1px solid #bdb9b9;
  cursor: pointer;
}

#op2 {
  padding-left: 30px;
  padding-right: 15px;
  cursor: pointer;
}
</style>
