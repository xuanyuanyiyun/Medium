import { useState } from 'react'
import { Plus, FileText, Video, Image, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const [recentProjects] = useState([
    { id: 1, name: 'AI技术趋势分析', type: 'article', status: 'completed', updatedAt: '2小时前' },
    { id: 2, name: '产品宣传视频', type: 'video', status: 'creating', updatedAt: '5小时前' },
    { id: 3, name: '端午活动海报', type: 'image_text', status: 'pending', updatedAt: '1天前' },
  ])

  const stats = [
    { label: '本周内容', value: '24', icon: FileText },
    { label: '视频产量', value: '8', icon: Video },
    { label: '分发平台', value: '5', icon: TrendingUp },
    { label: '总曝光量', value: '125K', icon: Image },
  ]

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">控制台</h1>
          <p className="text-gray-600 mt-1">欢迎使用 Media AI Agent</p>
        </div>
        <div className="flex gap-3">
          <button className="btn-secondary flex items-center gap-2">
            <FileText className="w-4 h-4" />
            创建文章
          </button>
          <button className="btn-secondary flex items-center gap-2">
            <Video className="w-4 h-4" />
            创建视频
          </button>
          <button className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" />
            新建项目
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
              </div>
              <stat.icon className="w-10 h-10 text-primary-500 opacity-20" />
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">最近项目</h2>
        <div className="space-y-4">
          {recentProjects.map((project) => (
            <div
              key={project.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center gap-4">
                {project.type === 'article' && <FileText className="w-5 h-5 text-blue-500" />}
                {project.type === 'video' && <Video className="w-5 h-5 text-purple-500" />}
                {project.type === 'image_text' && <Image className="w-5 h-5 text-green-500" />}
                <div>
                  <p className="font-medium text-gray-900">{project.name}</p>
                  <p className="text-sm text-gray-500">{project.updatedAt}</p>
                </div>
              </div>
              <span
                className={`px-3 py-1 text-sm rounded-full ${
                  project.status === 'completed'
                    ? 'bg-green-100 text-green-700'
                    : project.status === 'creating'
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {project.status === 'completed' ? '已完成' : project.status === 'creating' ? '创作中' : '待处理'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
