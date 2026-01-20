import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import TaskListView from '../views/TaskListView.vue'
import taskService from '../services/taskService'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// Mock依赖
vi.mock('../services/taskService')
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn()
  }
}))
vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: vi.fn()
  }))
}))

describe('TaskListView', () => {
  let wrapper
  const mockRouter = {
    push: vi.fn()
  }

  beforeEach(() => {
    // 重置mock
    vi.clearAllMocks()
    
    // 模拟router
    useRouter.mockReturnValue(mockRouter)
    
    // 模拟taskService返回值
    taskService.getTasks.mockResolvedValue({
      code: 200,
      message: 'success',
      data: {
        list: [
          { id: "t_001", file_type: "customs", unique_code: "UC001", flight_no: "NH123", declare_date: "2026-01-20", status: "success", created_at: "2026-01-20T01:02:03Z" },
          { id: "t_002", file_type: "delivery", unique_code: "UC002", flight_no: "", declare_date: "", status: "failed", created_at: "2026-01-20T02:10:11Z" }
        ],
        total: 2
      }
    })
    
    taskService.createTask.mockResolvedValue({
      code: 200,
      message: '任务创建成功',
      data: {
        id: "t_003",
        file_type: "customs",
        unique_code: "UC003",
        flight_no: "NH456",
        declare_date: "2026-01-21",
        status: "queued",
        created_at: "2026-01-21T09:00:00Z"
      }
    })
    
    // 挂载组件
    wrapper = mount(TaskListView)
  })

  it('should render task list correctly', async () => {
    // 等待异步数据加载
    await wrapper.vm.$nextTick()
    
    // 检查组件是否渲染
    expect(wrapper.exists()).toBe(true)
    
    // 检查标题是否正确
    expect(wrapper.text()).toContain('任务中心')
    
    // 检查是否调用了getTasks方法
    expect(taskService.getTasks).toHaveBeenCalled()
    
    // 检查任务列表是否渲染
    const rows = wrapper.findAll('.el-table__row')
    expect(rows.length).toBe(2)
  })

  it('should filter tasks by file type', async () => {
    // 等待异步数据加载
    await wrapper.vm.$nextTick()
    
    // 选择文件类型为customs
    await wrapper.findComponent({ name: 'ElSelect' }).setValue('customs')
    
    // 检查过滤后的数据
    const filteredTasks = wrapper.vm.filteredTasks
    expect(filteredTasks.length).toBe(1)
    expect(filteredTasks[0].file_type).toBe('customs')
  })

  it('should open create task dialog when clicking new task button', async () => {
    // 点击新建任务按钮
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 检查对话框是否打开
    expect(wrapper.vm.createDialog).toBe(true)
  })

  it('should create a new task successfully', async () => {
    // 打开创建任务对话框
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 填写表单
    wrapper.vm.createForm.unique_code = 'UC003'
    wrapper.vm.createForm.flight_no = 'NH456'
    wrapper.vm.createForm.declare_date = '2026-01-21'
    
    // 模拟表单验证通过
    const addFormRef = {
      validate: vi.fn().mockImplementation((callback) => callback(true))
    }
    wrapper.vm.addFormRef = addFormRef
    
    // 提交表单
    await wrapper.vm.submitCreate()
    
    // 检查是否调用了createTask方法
    expect(taskService.createTask).toHaveBeenCalled()
    
    // 检查是否显示成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('任务创建成功')
    
    // 检查是否跳转到任务详情页
    expect(mockRouter.push).toHaveBeenCalledWith('/task-detail/t_003')
    
    // 检查对话框是否关闭
    expect(wrapper.vm.createDialog).toBe(false)
  })

  it('should handle task creation failure', async () => {
    // 模拟创建任务失败
    taskService.createTask.mockRejectedValue(new Error('创建失败'))
    
    // 打开创建任务对话框
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 填写表单
    wrapper.vm.createForm.unique_code = 'UC003'
    
    // 模拟表单验证通过
    const addFormRef = {
      validate: vi.fn().mockImplementation((callback) => callback(true))
    }
    wrapper.vm.addFormRef = addFormRef
    
    // 提交表单
    await wrapper.vm.submitCreate()
    
    // 检查是否显示错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('任务创建失败')
  })
})
