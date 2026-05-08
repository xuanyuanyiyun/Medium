import { useState } from 'react'
import { CheckCircle, Circle, Loader2 } from 'lucide-react'

const PIPELINE_STAGES = [
  { id: 1, name: '选题', icon: '1', description: '智能热点分析' },
  { id: 2, name: '创作', icon: '2', description: 'AI内容生成' },
  { id: 3, name: '审核', icon: '3', description: '合规检查' },
  { id: 4, name: '分发', icon: '4', description: '一键发布' },
  { id: 5, name: '分析', icon: '5', description: '效果追踪' },
]

export default function ProfessionalMode() {
  const [currentStage, setCurrentStage] = useState(1)
  const [isRunning, setIsRunning] = useState(false)

  const handleStartPipeline = () => {
    setIsRunning(true)
    setCurrentStage(1)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">专业模式</h1>
        <p className="text-gray-600 mt-1">标准化流水线，适合大规模内容生产</p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-lg font-semibold">内容流水线</h2>
          {!isRunning && (
            <button onClick={handleStartPipeline} className="btn-primary">
              启动流水线
            </button>
          )}
        </div>

        <div className="flex items-center justify-between">
          {PIPELINE_STAGES.map((stage, index) => (
            <div key={stage.id} className="flex items-center">
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ${
                    currentStage > stage.id
                      ? 'bg-green-500 text-white'
                      : currentStage === stage.id
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {currentStage > stage.id ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : currentStage === stage.id ? (
                    isRunning ? (
                      <Loader2 className="w-6 h-6 animate-spin" />
                    ) : (
                      stage.icon
                    )
                  ) : (
                    stage.icon
                  )}
                </div>
                <p className="mt-2 font-medium text-gray-900">{stage.name}</p>
                <p className="text-sm text-gray-500">{stage.description}</p>
              </div>
              {index < PIPELINE_STAGES.length - 1 && (
                <div
                  className={`w-24 h-1 mx-4 rounded ${
                    currentStage > stage.id ? 'bg-green-500' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">当前任务</h3>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-gray-700">
              {currentStage === 1 && '正在分析热点话题...'}
              {currentStage === 2 && '正在生成文章内容...'}
              {currentStage === 3 && '正在进行合规审核...'}
              {currentStage === 4 && '正在分发至各平台...'}
              {currentStage === 5 && '正在收集效果数据...'}
            </p>
          </div>
        </div>

        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">任务日志</h3>
          <div className="space-y-2 font-mono text-sm">
            <p className="text-gray-600">[{new Date().toLocaleTimeString()}] 系统已启动</p>
            <p className="text-gray-600">[{new Date().toLocaleTimeString()}] 开始执行选题分析</p>
            <p className="text-green-600">[{new Date().toLocaleTimeString()}] 选题完成: AI技术突破</p>
          </div>
        </div>
      </div>
    </div>
  )
}
