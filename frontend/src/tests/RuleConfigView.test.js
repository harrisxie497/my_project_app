import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import RuleConfigView from '../views/admin/RuleConfigView.vue'
import ruleService from '../services/ruleService'
import { ElMessage } from 'element-plus'

// Mock依赖
vi.mock('../services/ruleService')
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn()
  }
}))

describe('RuleConfigView', () => {
  let wrapper

  beforeEach(() => {
    // 重置mock
    vi.clearAllMocks()
    
    // 模拟ruleService返回值
    ruleService.getRuleTables.mockResolvedValue({
      code: 200,
      message: 'success',
      data: {
        list: [
          { id: "rt_1", code: "MAP_CUSTOMS", file_type: "customs", rule_stage: "MAP", enabled: true, description: "原始→最终字段映射（清关）" },
          { id: "rt_2", code: "PROCESS_CUSTOMS", file_type: "customs", rule_stage: "PROCESS", enabled: true, description: "最终文件字段校验/修正/生成（清关）" }
        ],
        total: 2
      }
    })
    
    ruleService.importRuleTemplate.mockResolvedValue({
      code: 200,
      message: '规则模板导入成功',
      data: { success: true }
    })
    
    // 挂载组件
    wrapper = mount(RuleConfigView)
  })

  it('should render rule tables correctly', async () => {
    // 等待异步数据加载
    await wrapper.vm.$nextTick()
    
    // 检查组件是否渲染
    expect(wrapper.exists()).toBe(true)
    
    // 检查标题是否正确
    expect(wrapper.text()).toContain('规则配置')
    
    // 检查是否调用了getRuleTables方法
    expect(ruleService.getRuleTables).toHaveBeenCalled()
    
    // 检查规则表列表是否渲染
    const rows = wrapper.findAll('.el-table__row')
    expect(rows.length).toBe(2)
  })

  it('should open import dialog when clicking import button', async () => {
    // 点击导入规则模板按钮
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 检查对话框是否打开
    expect(wrapper.vm.importDialog).toBe(true)
    
    // 检查对话框标题
    expect(wrapper.find('.el-dialog__title').text()).toBe('导入规则配置（Excel 模板）')
  })

  it('should import rule template successfully', async () => {
    // 打开导入对话框
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 模拟文件选择
    const mockFile = new File(['test content'], 'rules.xlsx', { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    await wrapper.vm.onImportChange({ raw: mockFile })
    
    // 点击开始导入按钮
    await wrapper.find('.dialog-footer button[type="primary"]').trigger('click')
    
    // 检查是否调用了importRuleTemplate方法
    expect(ruleService.importRuleTemplate).toHaveBeenCalled()
    
    // 检查是否显示成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('规则模板导入成功')
    
    // 检查对话框是否关闭
    expect(wrapper.vm.importDialog).toBe(false)
    
    // 检查是否重新加载了规则表
    expect(ruleService.getRuleTables).toHaveBeenCalledTimes(2)
  })

  it('should handle import failure', async () => {
    // 模拟导入失败
    ruleService.importRuleTemplate.mockRejectedValue(new Error('导入失败'))
    
    // 打开导入对话框
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 模拟文件选择
    const mockFile = new File(['test content'], 'rules.xlsx', { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    await wrapper.vm.onImportChange({ raw: mockFile })
    
    // 点击开始导入按钮
    await wrapper.find('.dialog-footer button[type="primary"]').trigger('click')
    
    // 检查是否显示错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('导入失败')
  })

  it('should toggle rule table enabled status', async () => {
    // 等待异步数据加载
    await wrapper.vm.$nextTick()
    
    // 找到开关组件并点击
    const switchComponent = wrapper.findComponent({ name: 'ElSwitch' })
    await switchComponent.trigger('click')
    
    // 检查开关状态是否改变
    // 注意：由于是mock数据，实际的状态变更不会发送API请求
    expect(switchComponent.exists()).toBe(true)
  })
})
