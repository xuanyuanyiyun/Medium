import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ProfessionalMode from './pages/ProfessionalMode'
import CustomMode from './pages/CustomMode'
import ContentLibrary from './pages/ContentLibrary'
import DistributionCenter from './pages/DistributionCenter'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-primary-600">
                  Media AI Agent
                </h1>
                <div className="ml-10 flex space-x-4">
                  <Link to="/" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    首页
                  </Link>
                  <Link to="/professional" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    专业模式
                  </Link>
                  <Link to="/custom" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    自定义模式
                  </Link>
                  <Link to="/library" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    内容库
                  </Link>
                  <Link to="/distribution" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    分发中心
                  </Link>
                  <Link to="/analytics" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    数据分析
                  </Link>
                  <Link to="/settings" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    设置
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/professional" element={<ProfessionalMode />} />
            <Route path="/custom" element={<CustomMode />} />
            <Route path="/library" element={<ContentLibrary />} />
            <Route path="/distribution" element={<DistributionCenter />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
