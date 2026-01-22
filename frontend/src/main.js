import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入mock服务（已注释，使用真实API）
// import './mock/mockService'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.mount('#app')
