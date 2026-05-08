import { useState } from 'react'
import { Plus, Trash2, GripVertical } from 'lucide-react'

const MODULES = {
  topic: { name: '选题模块', items: ['热点聚合', '趋势追踪', '选题建议'] },
  creation: { name: '创作模块', items: ['文章创作', '视频创作', '图文创作'] },
  editing: { name: '编辑模块', items: ['智能剪辑', '字幕生成', '多语翻译'] },
  review: { name: '审核模块', items: ['合规检查', '事实核查', '敏感词过滤'] },
  distribution: { name: '分发模块', items: ['平台适配', '定时发布', '多平台同步'] },
}

export default function CustomMode() {
  const [workflow, setWorkflow] = useState<string[]>([])

  const handleAddModule = (moduleName: string) => {
    setWorkflow([...workflow, moduleName])
  }

  const handleRemoveModule = (index: number) => {
    setWorkflow(workflow.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">自定义模式</h1>
        <p className="text-gray-600 mt-1">模块化组装，按需配置创作流程</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">模块库</h2>
            <div className="space-y-4">
              {Object.entries(MODULES).map(([key, module]) => (
                <div key={key}>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">{module.name}</h3>
                  <div className="space-y-2">
                    {module.items.map((item) => (
                      <button
                        key={item}
                        onClick={() => handleAddModule(item)}
                        className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-lg flex items-center justify-between"
                      >
                        <span>{item}</span>
                        <Plus className="w-4 h-4 text-gray-400" />
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">工作流画布</h2>
            {workflow.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <p>从左侧模块库拖拽或点击添加模块</p>
              </div>
            ) : (
              <div className="space-y-4">
                {workflow.map((module, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg"
                  >
                    <GripVertical className="w-5 h-5 text-gray-400 cursor-move" />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{module}</p>
                      <p className="text-sm text-gray-500">模块 {index + 1}</p>
                    </div>
                    <button
                      onClick={() => handleRemoveModule(index)}
                      className="p-2 text-gray-400 hover:text-red-500"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                    {index < workflow.length - 1 && (
                      <div className="absolute left-1/2 -translate-x-1/2">
                        <div className="w-0.5 h-4 bg-gray-300" />
                      </div>
                    )}
                  </div>
                ))}
                
                <button className="btn-primary w-full mt-6">
                  执行工作流
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
