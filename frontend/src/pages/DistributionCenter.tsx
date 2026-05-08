import { useState } from 'react'
import { CheckCircle, Clock, AlertCircle, Send, Calendar, RotateCcw, ChevronDown, RefreshCw } from 'lucide-react'

interface Platform {
  id: string
  name: string
  icon: string
  color: string
  connected: boolean
  lastSync?: string
}

interface DistributionRecord {
  id: number
  title: string
  platform: string
  status: 'published' | 'pending' | 'failed' | 'scheduled'
  publishedAt?: string
  scheduledAt?: string
  views?: number
  error?: string
}

const PLATFORMS: Platform[] = [
  { id: 'wechat', name: '微信公众号', icon: '💚', color: 'bg-emerald-500', connected: true, lastSync: '2小时前' },
  { id: 'weibo', name: '微博', icon: '🔴', color: 'bg-red-500', connected: true, lastSync: '1小时前' },
  { id: 'zhihu', name: '知乎', icon: '🔵', color: 'bg-blue-500', connected: true, lastSync: '30分钟前' },
  { id: 'xiaohongshu', name: '小红书', icon: '🔴', color: 'bg-rose-500', connected: true, lastSync: '45分钟前' },
  { id: 'douyin', name: '抖音', icon: '⚫', color: 'bg-gray-900', connected: true, lastSync: '15分钟前' },
  { id: 'kuaishou', name: '快手', icon: '🟢', color: 'bg-green-500', connected: false },
  { id: 'bilibili', name: 'B站', icon: '💗', color: 'bg-pink-600', connected: true, lastSync: '1小时前' },
  { id: 'toutiao', name: '今日头条', icon: '🟠', color: 'bg-orange-500', connected: false },
]

const mockDistributions: DistributionRecord[] = [
  { id: 1, title: 'AI技术趋势深度分析：从GPT到多模态大模型', platform: 'wechat', status: 'published', publishedAt: '2024-01-15 14:30', views: 8560 },
  { id: 2, title: 'AI技术趋势深度分析：从GPT到多模态大模型', platform: 'weibo', status: 'published', publishedAt: '2024-01-15 14:32', views: 23400 },
  { id: 3, title: 'AI技术趋势深度分析：从GPT到多模态大模型', platform: 'douyin', status: 'published', publishedAt: '2024-01-15 14:35', views: 156000 },
  { id: 4, title: '2024年新媒体营销策略白皮书', platform: 'zhihu', status: 'scheduled', scheduledAt: '2024-01-16 10:00' },
  { id: 5, title: '端午节活动营销图文素材', platform: 'xiaohongshu', status: 'pending' },
  { id: 6, title: '企业品牌宣传短片', platform: 'bilibili', status: 'failed', error: '视频文件格式不支持' },
]

const statusConfig = {
  published: { label: '已发布', icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-100' },
  pending: { label: '待发布', icon: Clock, color: 'text-amber-600', bg: 'bg-amber-100' },
  scheduled: { label: '定时发布', icon: Calendar, color: 'text-sky-600', bg: 'bg-sky-100' },
  failed: { label: '发布失败', icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-100' },
}

export default function DistributionCenter() {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['wechat', 'weibo'])
  const [distributions] = useState<DistributionRecord[]>(mockDistributions)
  const [platforms] = useState<Platform[]>(PLATFORMS)
  const [showScheduleModal, setShowScheduleModal] = useState(false)
  const [scheduledTime, setScheduledTime] = useState('')
  const [isPublishing, setIsPublishing] = useState(false)
  const [publishingProgress, setPublishingProgress] = useState(0)

  const togglePlatform = (platformId: string) => {
    const platform = platforms.find(p => p.id === platformId)
    if (!platform?.connected) return
    
    setSelectedPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(p => p !== platformId)
        : [...prev, platformId]
    )
  }

  const handlePublish = async () => {
    if (selectedPlatforms.length === 0) return
    
    setIsPublishing(true)
    setPublishingProgress(0)
    
    for (let i = 0; i < selectedPlatforms.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800))
      setPublishingProgress(((i + 1) / selectedPlatforms.length) * 100)
    }
    
    setIsPublishing(false)
  }

  const handleSchedule = () => {
    if (selectedPlatforms.length === 0 || !scheduledTime) return
    setShowScheduleModal(false)
    setScheduledTime('')
  }

  const getPlatformIcon = (platformId: string) => {
    return platforms.find(p => p.id === platformId)?.icon || '📱'
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">分发中心</h1>
        <p className="text-gray-500 mt-1">一键分发内容至多个平台，支持定时发布和状态追踪</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-gray-900">选择分发平台</h2>
              <span className="text-sm text-gray-500">已选择 {selectedPlatforms.length} 个平台</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {platforms.map((platform) => {
                const isSelected = selectedPlatforms.includes(platform.id)
                const isConnected = platform.connected
                return (
                  <button
                    key={platform.id}
                    onClick={() => togglePlatform(platform.id)}
                    disabled={!isConnected}
                    className={`relative p-4 rounded-xl border-2 transition-all ${
                      !isConnected
                        ? 'border-gray-200 opacity-50 cursor-not-allowed'
                        : isSelected
                        ? 'border-sky-500 bg-sky-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="text-3xl mb-2">{platform.icon}</div>
                    <p className="text-sm font-medium text-gray-900">{platform.name}</p>
                    {isConnected ? (
                      <div className="mt-2 flex items-center gap-1">
                        <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                        <span className="text-xs text-gray-500">已连接</span>
                      </div>
                    ) : (
                      <div className="mt-2 flex items-center gap-1">
                        <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                        <span className="text-xs text-gray-500">未连接</span>
                      </div>
                    )}
                    {isSelected && isConnected && (
                      <div className="absolute -top-2 -right-2 w-6 h-6 bg-sky-500 rounded-full flex items-center justify-center">
                        <CheckCircle className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </button>
                )
              })}
            </div>
            
            <div className="mt-6 pt-6 border-t flex flex-wrap gap-3">
              <button
                onClick={handlePublish}
                disabled={selectedPlatforms.length === 0 || isPublishing}
                className="px-6 py-3 bg-sky-500 text-white rounded-lg hover:bg-sky-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isPublishing ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    发布中... {Math.round(publishingProgress)}%
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    一键发布
                  </>
                )}
              </button>
              <button
                onClick={() => setShowScheduleModal(true)}
                disabled={selectedPlatforms.length === 0}
                className="px-6 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Calendar className="w-5 h-5" />
                定时发布
              </button>
            </div>

            {isPublishing && (
              <div className="mt-4">
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-sky-500 h-full transition-all duration-300"
                    style={{ width: `${publishingProgress}%` }}
                  ></div>
                </div>
                <div className="flex justify-between mt-2 text-xs text-gray-500">
                  {selectedPlatforms.map(platformId => {
                    const progress = selectedPlatforms.indexOf(platformId) + 1
                    const isComplete = (progress / selectedPlatforms.length) * 100 <= publishingProgress
                    return (
                      <span key={platformId} className={isComplete ? 'text-emerald-600' : ''}>
                        {getPlatformIcon(platformId)} {platforms.find(p => p.id === platformId)?.name}
                        {isComplete && ' ✓'}
                      </span>
                    )
                  })}
                </div>
              </div>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-gray-900">分发记录</h2>
              <div className="flex gap-2">
                <select className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg">
                  <option value="all">全部平台</option>
                  {platforms.filter(p => p.connected).map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
                <select className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg">
                  <option value="all">全部状态</option>
                  <option value="published">已发布</option>
                  <option value="pending">待发布</option>
                  <option value="scheduled">定时发布</option>
                  <option value="failed">发布失败</option>
                </select>
              </div>
            </div>
            <div className="space-y-3">
              {distributions.map((dist) => {
                const status = statusConfig[dist.status]
                const StatusIcon = status.icon
                const platform = platforms.find(p => p.id === dist.platform)
                return (
                  <div key={dist.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center gap-4">
                      <span className="text-2xl">{platform?.icon}</span>
                      <div>
                        <p className="font-medium text-gray-900 line-clamp-1">{dist.title}</p>
                        <p className="text-sm text-gray-500">{platform?.name}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className={`flex items-center gap-2 ${status.color}`}>
                        <StatusIcon className="w-4 h-4" />
                        <span className="text-sm font-medium">{status.label}</span>
                      </div>
                      {dist.views && (
                        <span className="text-sm text-gray-500">
                          {dist.views.toLocaleString()} 阅读
                        </span>
                      )}
                      {dist.scheduledAt && (
                        <span className="text-sm text-gray-500">
                          {dist.scheduledAt}
                        </span>
                      )}
                      {dist.error && (
                        <span className="text-sm text-red-500">
                          {dist.error}
                        </span>
                      )}
                      <div className="flex gap-2">
                        {dist.status === 'failed' && (
                          <button className="p-2 text-sky-500 hover:bg-sky-50 rounded-lg" title="重试">
                            <RotateCcw className="w-4 h-4" />
                          </button>
                        )}
                        {dist.status === 'scheduled' && (
                          <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg" title="取消定时">
                            <AlertCircle className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="font-semibold text-gray-900 mb-4">分发统计</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">总发布次数</span>
                <span className="font-semibold text-gray-900">156</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">成功发布</span>
                <span className="font-semibold text-emerald-600">142</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">待发布</span>
                <span className="font-semibold text-amber-600">8</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">发布失败</span>
                <span className="font-semibold text-red-600">6</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="font-semibold text-gray-900 mb-4">平台连接状态</h2>
            <div className="space-y-3">
              {platforms.slice(0, 6).map(platform => (
                <div key={platform.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{platform.icon}</span>
                    <span className="text-sm text-gray-700">{platform.name}</span>
                  </div>
                  {platform.connected ? (
                    <div className="flex items-center gap-1 text-emerald-600">
                      <CheckCircle className="w-4 h-4" />
                      <span className="text-xs">{platform.lastSync}</span>
                    </div>
                  ) : (
                    <button className="text-xs text-sky-500 hover:text-sky-600">
                      立即连接
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button className="w-full mt-4 py-2 text-sm text-sky-500 hover:text-sky-600 border border-dashed border-sky-300 rounded-lg">
              查看全部 8 个平台
            </button>
          </div>
        </div>
      </div>

      {showScheduleModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">定时发布设置</h3>
            <p className="text-gray-500 text-sm mb-4">
              选择发布时间，内容将在指定时间自动发布到选中的 {selectedPlatforms.length} 个平台
            </p>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                定时发布时间
              </label>
              <input
                type="datetime-local"
                value={scheduledTime}
                onChange={(e) => setScheduledTime(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowScheduleModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                取消
              </button>
              <button
                onClick={handleSchedule}
                disabled={!scheduledTime}
                className="px-6 py-2 bg-sky-500 text-white rounded-lg hover:bg-sky-600 disabled:opacity-50"
              >
                确认定时
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
