import { useState } from 'react'
import { Key, Globe, Bell, Shield, User, Database, Save, Eye, EyeOff, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react'

interface PlatformConnection {
  id: string
  name: string
  icon: string
  connected: boolean
  lastSync?: string
  credentials?: Record<string, string>
}

const PLATFORMS: PlatformConnection[] = [
  { id: 'wechat', name: '微信公众号', icon: '💚', connected: true, lastSync: '2小时前', credentials: { appId: 'wx_***', appSecret: '****' } },
  { id: 'weibo', name: '微博', icon: '🔴', connected: true, lastSync: '1小时前', credentials: { clientId: 'weibo_***', clientSecret: '****' } },
  { id: 'zhihu', name: '知乎', icon: '🔵', connected: false },
  { id: 'xiaohongshu', name: '小红书', icon: '🔴', connected: true, lastSync: '30分钟前', credentials: { cookie: 'xhs_***' } },
  { id: 'douyin', name: '抖音', icon: '⚫', connected: false },
  { id: 'kuaishou', name: '快手', icon: '🟢', connected: false },
  { id: 'bilibili', name: 'B站', icon: '💗', connected: true, lastSync: '1小时前', credentials: { sessData: 'bilibili_***' } },
  { id: 'toutiao', name: '今日头条', icon: '🟠', connected: false },
]

export default function Settings() {
  const [apiKeys, setApiKeys] = useState({
    openai: 'sk-••••••••••••••••••••••••••••••••',
    anthropic: 'sk-ant-••••••••••••••••••••••••••',
    midjourney: '',
  })
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({})
  const [platforms, setPlatforms] = useState<PlatformConnection[]>(PLATFORMS)
  const [notifications, setNotifications] = useState({
    distributionSuccess: true,
    reviewFailed: true,
    dailyReport: false,
    weeklySummary: true,
  })
  const [activeTab, setActiveTab] = useState('api')
  const [isSaving, setIsSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')

  const toggleShowKey = (key: string) => {
    setShowKeys(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const handleSave = async () => {
    setIsSaving(true)
    await new Promise(resolve => setTimeout(resolve, 1500))
    setIsSaving(false)
    setSaveMessage('设置已保存')
    setTimeout(() => setSaveMessage(''), 3000)
  }

  const handleConnectPlatform = (platformId: string) => {
    const platform = platforms.find(p => p.id === platformId)
    if (!platform) return
    if (platform.connected) {
      setPlatforms(prev => prev.map(p => 
        p.id === platformId ? { ...p, connected: false, lastSync: undefined, credentials: undefined } : p
      ))
    } else {
      window.open(`/settings/platforms/${platformId}/connect`, '_blank', 'width=600,height=700')
    }
  }

  const tabs = [
    { id: 'api', label: 'API 密钥', icon: Key },
    { id: 'platforms', label: '平台连接', icon: Globe },
    { id: 'notifications', label: '通知设置', icon: Bell },
    { id: 'security', label: '安全设置', icon: Shield },
    { id: 'account', label: '账户信息', icon: User },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">设置</h1>
        <p className="text-gray-500 mt-1">配置 API 密钥、平台连接和通知偏好</p>
      </div>

      <div className="flex gap-6">
        <div className="w-56 flex-shrink-0">
          <nav className="space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-sky-50 text-sky-600'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        <div className="flex-1">
          {activeTab === 'api' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-sky-100 rounded-lg">
                    <Key className="w-5 h-5 text-sky-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">AI 服务 API 密钥</h2>
                    <p className="text-sm text-gray-500">配置 OpenAI、Claude 等 AI 服务的访问密钥</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">OpenAI API Key</label>
                    <div className="relative">
                      <input
                        type={showKeys.openai ? 'text' : 'password'}
                        value={apiKeys.openai}
                        onChange={(e) => setApiKeys({ ...apiKeys, openai: e.target.value })}
                        className="w-full px-4 py-2.5 pr-20 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                        placeholder="sk-..."
                      />
                      <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                        <button
                          onClick={() => toggleShowKey('openai')}
                          className="p-1.5 text-gray-400 hover:text-gray-600"
                        >
                          {showKeys.openai ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                        <span className="px-2 py-1 bg-emerald-100 text-emerald-600 text-xs rounded">已配置</span>
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs text-gray-500">用于 GPT-4、GPT-3.5 等模型的调用</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Anthropic API Key</label>
                    <div className="relative">
                      <input
                        type={showKeys.anthropic ? 'text' : 'password'}
                        value={apiKeys.anthropic}
                        onChange={(e) => setApiKeys({ ...apiKeys, anthropic: e.target.value })}
                        className="w-full px-4 py-2.5 pr-20 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                        placeholder="sk-ant-..."
                      />
                      <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                        <button
                          onClick={() => toggleShowKey('anthropic')}
                          className="p-1.5 text-gray-400 hover:text-gray-600"
                        >
                          {showKeys.anthropic ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                        <span className="px-2 py-1 bg-emerald-100 text-emerald-600 text-xs rounded">已配置</span>
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs text-gray-500">用于 Claude 3 等模型的调用</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Midjourney API Key</label>
                    <div className="relative">
                      <input
                        type={showKeys.midjourney ? 'text' : 'password'}
                        value={apiKeys.midjourney}
                        onChange={(e) => setApiKeys({ ...apiKeys, midjourney: e.target.value })}
                        className="w-full px-4 py-2.5 pr-20 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                        placeholder="输入 Midjourney API Key"
                      />
                      <div className="absolute right-2 top-1/2 -translate-y-1/2">
                        <button
                          onClick={() => toggleShowKey('midjourney')}
                          className="p-1.5 text-gray-400 hover:text-gray-600"
                        >
                          {showKeys.midjourney ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs text-gray-500">用于图像生成服务（可选）</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'platforms' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-emerald-100 rounded-lg">
                    <Globe className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">内容平台连接</h2>
                    <p className="text-sm text-gray-500">管理各内容平台的授权和连接状态</p>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {platforms.map((platform) => (
                    <div key={platform.id} className="p-4 border border-gray-200 rounded-xl hover:border-gray-300 transition-colors">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">{platform.icon}</span>
                          <div>
                            <p className="font-medium text-gray-900">{platform.name}</p>
                            {platform.connected ? (
                              <div className="flex items-center gap-2 mt-1">
                                <span className="text-xs text-emerald-600 flex items-center gap-1">
                                  <CheckCircle className="w-3 h-3" />
                                  已连接
                                </span>
                                {platform.lastSync && (
                                  <span className="text-xs text-gray-400">
                                    · {platform.lastSync}
                                  </span>
                                )}
                              </div>
                            ) : (
                              <span className="text-xs text-gray-400 mt-1">未连接</span>
                            )}
                          </div>
                        </div>
                        <button
                          onClick={() => handleConnectPlatform(platform.id)}
                          className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                            platform.connected
                              ? 'bg-red-50 text-red-600 hover:bg-red-100'
                              : 'bg-sky-50 text-sky-600 hover:bg-sky-100'
                          }`}
                        >
                          {platform.connected ? '断开' : '连接'}
                        </button>
                      </div>
                      {platform.connected && platform.credentials && (
                        <div className="mt-3 pt-3 border-t border-gray-100">
                          <p className="text-xs text-gray-500 mb-2">授权信息</p>
                          <div className="space-y-1">
                            {Object.entries(platform.credentials).map(([key, value]) => (
                              <div key={key} className="flex items-center justify-between text-xs">
                                <span className="text-gray-500">{key}</span>
                                <span className="text-gray-700 font-mono">{value}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                <button className="mt-4 w-full py-3 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 hover:border-gray-400 hover:text-gray-600 transition-colors flex items-center justify-center gap-2">
                  <span className="text-xl">+</span>
                  添加更多平台
                </button>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-amber-100 rounded-lg">
                    <Bell className="w-5 h-5 text-amber-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">通知偏好</h2>
                    <p className="text-sm text-gray-500">选择您希望接收的通知类型</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <label className="flex items-center justify-between p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-medium text-gray-900">分发成功通知</p>
                      <p className="text-sm text-gray-500 mt-1">当内容成功发布到平台时发送通知</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={notifications.distributionSuccess}
                      onChange={(e) => setNotifications({ ...notifications, distributionSuccess: e.target.checked })}
                      className="w-5 h-5 text-sky-600 rounded"
                    />
                  </label>
                  <label className="flex items-center justify-between p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-medium text-gray-900">审核失败通知</p>
                      <p className="text-sm text-gray-500 mt-1">当内容审核不通过或出现问题时发送通知</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={notifications.reviewFailed}
                      onChange={(e) => setNotifications({ ...notifications, reviewFailed: e.target.checked })}
                      className="w-5 h-5 text-sky-600 rounded"
                    />
                  </label>
                  <label className="flex items-center justify-between p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-medium text-gray-900">每日数据报告</p>
                      <p className="text-sm text-gray-500 mt-1">每日发送内容表现数据摘要</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={notifications.dailyReport}
                      onChange={(e) => setNotifications({ ...notifications, dailyReport: e.target.checked })}
                      className="w-5 h-5 text-sky-600 rounded"
                    />
                  </label>
                  <label className="flex items-center justify-between p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                    <div>
                      <p className="font-medium text-gray-900">每周数据汇总</p>
                      <p className="text-sm text-gray-500 mt-1">每周一发送上周内容数据汇总报告</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={notifications.weeklySummary}
                      onChange={(e) => setNotifications({ ...notifications, weeklySummary: e.target.checked })}
                      className="w-5 h-5 text-sky-600 rounded"
                    />
                  </label>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="font-semibold text-gray-900 mb-4">通知渠道</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 border border-gray-200 rounded-xl text-center">
                    <div className="text-2xl mb-2">📧</div>
                    <p className="font-medium text-gray-900">邮件</p>
                    <p className="text-sm text-gray-500 mt-1">通知到注册邮箱</p>
                    <span className="inline-block mt-2 px-2 py-0.5 bg-emerald-100 text-emerald-600 text-xs rounded">已启用</span>
                  </div>
                  <div className="p-4 border border-gray-200 rounded-xl text-center">
                    <div className="text-2xl mb-2">💬</div>
                    <p className="font-medium text-gray-900">微信</p>
                    <p className="text-sm text-gray-500 mt-1">通过公众号推送</p>
                    <span className="inline-block mt-2 px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">未配置</span>
                  </div>
                  <div className="p-4 border border-gray-200 rounded-xl text-center">
                    <div className="text-2xl mb-2">🔔</div>
                    <p className="font-medium text-gray-900">站内通知</p>
                    <p className="text-sm text-gray-500 mt-1">系统消息中心</p>
                    <span className="inline-block mt-2 px-2 py-0.5 bg-emerald-100 text-emerald-600 text-xs rounded">已启用</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-violet-100 rounded-lg">
                    <Shield className="w-5 h-5 text-violet-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">安全设置</h2>
                    <p className="text-sm text-gray-500">管理账户安全和权限</p>
                  </div>
                </div>
                <div className="space-y-6">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">修改密码</h3>
                    <div className="space-y-3">
                      <input
                        type="password"
                        placeholder="当前密码"
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500"
                      />
                      <input
                        type="password"
                        placeholder="新密码"
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500"
                      />
                      <input
                        type="password"
                        placeholder="确认新密码"
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500"
                      />
                    </div>
                  </div>
                  <div className="pt-4 border-t">
                    <h3 className="font-medium text-gray-900 mb-3">两步验证</h3>
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-amber-100 rounded-lg">
                          <AlertCircle className="w-5 h-5 text-amber-600" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">未启用</p>
                          <p className="text-sm text-gray-500">建议启用两步验证以增强账户安全</p>
                        </div>
                      </div>
                      <button className="px-4 py-2 bg-sky-50 text-sky-600 rounded-lg hover:bg-sky-100">
                        启用
                      </button>
                    </div>
                  </div>
                  <div className="pt-4 border-t">
                    <h3 className="font-medium text-gray-900 mb-3">API 访问日志</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center py-2 text-sm">
                        <span className="text-gray-600">API 调用（今日）</span>
                        <span className="font-medium">1,234 次</span>
                      </div>
                      <div className="flex justify-between items-center py-2 text-sm">
                        <span className="text-gray-600">最后活跃</span>
                        <span className="font-medium">2 分钟前</span>
                      </div>
                      <div className="flex justify-between items-center py-2 text-sm">
                        <span className="text-gray-600">IP 地址</span>
                        <span className="font-medium font-mono">192.168.1.***</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'account' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-sky-100 rounded-lg">
                    <User className="w-5 h-5 text-sky-600" />
                  </div>
                  <div>
                    <h2 className="font-semibold text-gray-900">账户信息</h2>
                    <p className="text-sm text-gray-500">查看和管理您的账户详情</p>
                  </div>
                </div>
                <div className="flex items-center gap-6 mb-6 pb-6 border-b">
                  <div className="w-20 h-20 bg-gradient-to-br from-sky-400 to-sky-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                    AI
                  </div>
                  <div>
                    <p className="text-xl font-semibold text-gray-900">Administrator</p>
                    <p className="text-gray-500">admin@media-ai-agent.com</p>
                    <span className="inline-block mt-2 px-2 py-0.5 bg-sky-100 text-sky-600 text-xs rounded">
                      管理员
                    </span>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3">
                    <span className="text-gray-600">账户类型</span>
                    <span className="font-medium">专业版</span>
                  </div>
                  <div className="flex justify-between items-center py-3">
                    <span className="text-gray-600">注册时间</span>
                    <span className="font-medium">2024年1月1日</span>
                  </div>
                  <div className="flex justify-between items-center py-3">
                    <span className="text-gray-600">剩余配额</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="w-3/4 h-full bg-sky-500"></div>
                      </div>
                      <span className="text-sm font-medium">750/1000</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="font-semibold text-gray-900 mb-4">使用统计</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-sky-50 rounded-xl text-center">
                    <p className="text-2xl font-bold text-sky-600">156</p>
                    <p className="text-sm text-gray-500 mt-1">已发布内容</p>
                  </div>
                  <div className="p-4 bg-emerald-50 rounded-xl text-center">
                    <p className="text-2xl font-bold text-emerald-600">8</p>
                    <p className="text-sm text-gray-500 mt-1">已连接平台</p>
                  </div>
                  <div className="p-4 bg-amber-50 rounded-xl text-center">
                    <p className="text-2xl font-bold text-amber-600">23</p>
                    <p className="text-sm text-gray-500 mt-1">本月项目</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="mt-6 flex items-center justify-between">
            {saveMessage && (
              <div className="flex items-center gap-2 text-emerald-600">
                <CheckCircle className="w-5 h-5" />
                <span>{saveMessage}</span>
              </div>
            )}
            <div className="ml-auto">
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="px-6 py-2.5 bg-sky-500 text-white rounded-lg hover:bg-sky-600 disabled:opacity-50 flex items-center gap-2"
              >
                {isSaving ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    保存中...
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    保存设置
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
