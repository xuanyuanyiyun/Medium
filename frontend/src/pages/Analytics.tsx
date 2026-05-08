import { useState } from 'react'
import { TrendingUp, TrendingDown, Eye, Heart, MessageCircle, Share2, Download, RefreshCw } from 'lucide-react'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface MetricCardProps {
  title: string
  value: string | number
  change: number
  changeLabel: string
  icon: React.ReactNode
  color: string
}

const metricCards: MetricCardProps[] = [
  { title: '总浏览量', value: '1,258,900', change: 23.5, changeLabel: '较上月', icon: <Eye className="w-6 h-6" />, color: 'sky' },
  { title: '总点赞数', value: '125,800', change: 18.2, changeLabel: '较上月', icon: <Heart className="w-6 h-6" />, color: 'rose' },
  { title: '总评论数', value: '34,560', change: -5.1, changeLabel: '较上月', icon: <MessageCircle className="w-6 h-6" />, color: 'amber' },
  { title: '总分享数', value: '45,230', change: 12.8, changeLabel: '较上月', icon: <Share2 className="w-6 h-6" />, color: 'emerald' },
]

const weeklyData = [
  { date: '01-08', views: 4200, likes: 380, comments: 85, shares: 62 },
  { date: '01-09', views: 5800, likes: 520, comments: 112, shares: 88 },
  { date: '01-10', views: 4900, likes: 445, comments: 96, shares: 71 },
  { date: '01-11', views: 6300, likes: 580, comments: 128, shares: 95 },
  { date: '01-12', views: 7800, likes: 720, comments: 156, shares: 118 },
  { date: '01-13', views: 8200, likes: 760, comments: 168, shares: 132 },
  { date: '01-14', views: 9100, likes: 840, comments: 185, shares: 148 },
]

const platformData = [
  { name: '微信', value: 35, color: '#10b981' },
  { name: '微博', value: 25, color: '#ef4444' },
  { name: '抖音', value: 20, color: '#6366f1' },
  { name: '小红书', value: 12, color: '#ec4899' },
  { name: 'B站', value: 8, color: '#f43f5e' },
]

const contentTypeData = [
  { type: '文章', published: 45, views: 580000, engagement: 6.8 },
  { type: '视频', published: 28, views: 420000, engagement: 12.3 },
  { type: '图文', published: 38, views: 258900, engagement: 9.2 },
]

const topContentData = [
  { title: 'AI技术趋势深度分析：从GPT到多模态大模型', platform: 'wechat', views: 85600, engagement: 8.5, likes: 7280 },
  { title: '2024年新媒体营销策略完整指南', platform: 'weibo', views: 124000, engagement: 6.2, likes: 8920 },
  { title: '产品功能介绍短片', platform: 'douyin', views: 356000, engagement: 15.8, likes: 56200 },
  { title: '端午节营销素材合集', platform: 'xiaohongshu', views: 89000, engagement: 11.2, likes: 9980 },
  { title: '企业品牌故事视频', platform: 'bilibili', views: 45600, engagement: 9.8, likes: 4470 },
]

const platformIcons: Record<string, string> = {
  wechat: '💚',
  weibo: '🔴',
  zhihu: '🔵',
  xiaohongshu: '🔴',
  douyin: '⚫',
  kuaishou: '🟢',
  bilibili: '💗',
  toutiao: '🟠',
}

const colorMap: Record<string, string> = {
  sky: 'bg-sky-100 text-sky-600',
  rose: 'bg-rose-100 text-rose-600',
  amber: 'bg-amber-100 text-amber-600',
  emerald: 'bg-emerald-100 text-emerald-600',
}

export default function Analytics() {
  const [timeRange, setTimeRange] = useState('7d')
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await new Promise(resolve => setTimeout(resolve, 1500))
    setIsRefreshing(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">数据分析</h1>
          <p className="text-gray-500 mt-1">追踪内容传播效果，优化运营策略</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500"
          >
            <option value="7d">最近7天</option>
            <option value="30d">最近30天</option>
            <option value="90d">最近90天</option>
          </select>
          <button
            onClick={handleRefresh}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <RefreshCw className={`w-5 h-5 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
          <button className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center gap-2">
            <Download className="w-5 h-5" />
            导出报告
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metricCards.map((metric) => (
          <div key={metric.title} className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div className={`p-3 rounded-xl ${colorMap[metric.color]}`}>
                {metric.icon}
              </div>
              <div className={`flex items-center gap-1 text-sm font-medium ${
                metric.change >= 0 ? 'text-emerald-600' : 'text-red-600'
              }`}>
                {metric.change >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                {Math.abs(metric.change)}%
              </div>
            </div>
            <div className="mt-4">
              <p className="text-sm text-gray-500">{metric.title}</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{metric.value}</p>
              <p className="text-xs text-gray-400 mt-1">{metric.changeLabel}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-semibold text-gray-900">数据趋势</h2>
            <div className="flex gap-4 text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="w-4 h-4 text-sky-600 rounded" />
                <span className="text-gray-600">浏览量</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="w-4 h-4 text-rose-600 rounded" />
                <span className="text-gray-600">点赞</span>
              </label>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={weeklyData}>
                <defs>
                  <linearGradient id="colorViews" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorLikes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                />
                <Area
                  type="monotone"
                  dataKey="views"
                  stroke="#0ea5e9"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorViews)"
                  name="浏览量"
                />
                <Area
                  type="monotone"
                  dataKey="likes"
                  stroke="#f43f5e"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorLikes)"
                  name="点赞"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="font-semibold text-gray-900 mb-6">平台分布</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={platformData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {platformData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            {platformData.map((item) => (
              <div key={item.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span className="text-gray-600">{item.name}</span>
                </div>
                <span className="font-medium text-gray-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="font-semibold text-gray-900 mb-6">内容类型对比</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={contentTypeData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" stroke="#9ca3af" fontSize={12} />
                <YAxis dataKey="type" type="category" stroke="#9ca3af" fontSize={12} width={60} />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                />
                <Legend />
                <Bar dataKey="published" fill="#0ea5e9" name="发布数量" radius={[0, 4, 4, 0]} />
                <Bar dataKey="views" fill="#8b5cf6" name="浏览量" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="font-semibold text-gray-900 mb-6">互动率概览</h2>
          <div className="space-y-6">
            {contentTypeData.map((item) => (
              <div key={item.type}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">{item.type}</span>
                  <span className="text-sm font-semibold text-sky-600">{item.engagement}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-3">
                  <div
                    className="bg-sky-500 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(item.engagement * 5, 100)}%` }}
                  ></div>
                </div>
                <div className="flex justify-between mt-1 text-xs text-gray-400">
                  <span>发布 {item.published} 篇</span>
                  <span>{(item.views / 1000).toFixed(0)}K 阅读</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-semibold text-gray-900">热门内容排行</h2>
          <div className="flex gap-2">
            <button className="px-3 py-1.5 text-sm bg-sky-50 text-sky-600 rounded-lg">浏览量</button>
            <button className="px-3 py-1.5 text-sm text-gray-500 hover:bg-gray-50 rounded-lg">互动率</button>
            <button className="px-3 py-1.5 text-sm text-gray-500 hover:bg-gray-50 rounded-lg">点赞数</button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4 font-medium text-gray-600 w-12">#</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">内容标题</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600 w-24">平台</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600 w-32">浏览量</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600 w-24">点赞</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600 w-24">互动率</th>
              </tr>
            </thead>
            <tbody>
              {topContentData.map((content, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-sm font-bold ${
                      index === 0 ? 'bg-amber-100 text-amber-600' :
                      index === 1 ? 'bg-gray-200 text-gray-600' :
                      index === 2 ? 'bg-orange-100 text-orange-600' :
                      'bg-gray-50 text-gray-500'
                    }`}>
                      {index + 1}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <p className="font-medium text-gray-900 line-clamp-1">{content.title}</p>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{platformIcons[content.platform]}</span>
                      <span className="text-sm text-gray-600 capitalize">{content.platform}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-900 font-medium">
                    {content.views.toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-gray-600">
                    {content.likes.toLocaleString()}
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-sky-50 text-sky-600 text-sm font-medium rounded">
                      {content.engagement}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
