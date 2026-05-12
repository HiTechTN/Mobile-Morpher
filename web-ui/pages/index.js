import { useState, useRef } from 'react'
import axios from 'axios'

const modes = [
  {
    id: 'express',
    name: 'Express',
    description: 'Transformation rapide',
    icon: '⚡'
  },
  {
    id: 'design',
    name: 'Design',
    description: 'Modification complète',
    icon: '🎨'
  },
  {
    id: 'developer',
    name: 'Developer',
    description: 'Pour développeurs',
    icon: '🔧'
  }
]

export default function Home() {
  const [mode, setMode] = useState('express')
  const [file, setFile] = useState(null)
  const [appName, setAppName] = useState('')
  const [packageId, setPackageId] = useState('')
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)

  const apiBase = process.env.API_URL || (typeof window !== 'undefined' ? `${window.location.protocol}//${window.location.hostname}:9000` : 'http://localhost:9000')

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.name.endsWith('.apk')) {
      setFile(droppedFile)
    } else {
      setError('Veuillez sélectionner un fichier APK')
    }
  }

  const handleUpload = async () => {
    setError('')
    setProgress(0)
    if (!file || !appName || !packageId) {
      setError('Veuillez remplir tous les champs')
      return
    }

    if (!packageId.match(/^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$/)) {
      setError('Format de Package ID invalide (ex: com.monapp.pro)')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      setProgress(20)
      const uploadRes = await axios.post(`${apiBase}/api/upload`, formData)
      const sessionId = uploadRes.data.session_id

      setProgress(50)
      const processRes = await axios.post(`${apiBase}/api/process/${sessionId}`, {
        new_app_name: appName,
        new_package_id: packageId,
        mode: mode
      })

      setProgress(100)
      setResult({ ...processRes.data, sessionId: sessionId })
    } catch (err) {
      console.error(err)
      setError(`Erreur: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setFile(null)
    setAppName('')
    setPackageId('')
    setResult(null)
    setError('')
    setProgress(0)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50"></div>
      
      <div className="relative container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4 shadow-lg shadow-purple-500/30">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Mobile-Morpher
          </h1>
          <p className="text-slate-400 text-lg">Transformez vos applications Android en quelques clics</p>
        </header>

        <div className="max-w-xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <span className="w-1 h-6 bg-blue-500 rounded-full"></span>
              Mode de transformation
            </h2>
            
            <div className="grid grid-cols-3 gap-3 mb-8">
              {modes.map((m) => (
                <button
                  key={m.id}
                  onClick={() => setMode(m.id)}
                  className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                    mode === m.id
                      ? 'border-blue-500 bg-blue-500/20 scale-105'
                      : 'border-slate-600 hover:border-slate-500 hover:bg-slate-700/30'
                  }`}
                >
                  <div className="text-2xl mb-2">{m.icon}</div>
                  <div className="font-medium text-sm">{m.name}</div>
                  <div className="text-xs text-slate-400">{m.description}</div>
                </button>
              ))}
            </div>

            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <span className="w-1 h-6 bg-purple-500 rounded-full"></span>
              Fichier APK
            </h2>

            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 mb-6 ${
                isDragging
                  ? 'border-blue-500 bg-blue-500/20'
                  : file
                  ? 'border-green-500 bg-green-500/10'
                  : 'border-slate-600 hover:border-slate-500 hover:bg-slate-700/30'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".apk"
                onChange={(e) => setFile(e.target.files[0])}
                className="hidden"
              />
              {file ? (
                <div className="flex items-center justify-center gap-3">
                  <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-green-400 font-medium">{file.name}</span>
                </div>
              ) : (
                <div>
                  <svg className="w-12 h-12 mx-auto mb-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p className="text-slate-400">Glissez votre fichier APK ici</p>
                  <p className="text-slate-500 text-sm mt-1">ou cliquez pour parcourir</p>
                </div>
              )}
            </div>

            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <span className="w-1 h-6 bg-pink-500 rounded-full"></span>
              Configuration
            </h2>

            <div className="space-y-4 mb-8">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Nom de l'application
                </label>
                <input
                  type="text"
                  placeholder="Mon Application"
                  value={appName}
                  onChange={(e) => setAppName(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg bg-slate-700/50 border border-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all outline-none placeholder-slate-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Package ID
                </label>
                <input
                  type="text"
                  placeholder="com.monapp.pro"
                  value={packageId}
                  onChange={(e) => setPackageId(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg bg-slate-700/50 border border-slate-600 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all outline-none placeholder-slate-500"
                />
                <p className="text-xs text-slate-500 mt-1">Format: com.nomentreprise.nomapp</p>
              </div>
            </div>

            {loading && (
              <div className="mb-6">
                <div className="flex justify-between text-sm text-slate-400 mb-2">
                  <span>Progression</span>
                  <span>{progress}%</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {error && (
              <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-300 flex items-center gap-3">
                <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {error}
              </div>
            )}

            {result ? (
              <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-6 text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-green-500/20 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-green-400 mb-2">Transformation réussie!</h3>
                <p className="text-slate-400 mb-4">Votre APK est prêt au téléchargement</p>
                <a
                  href={`${apiBase}/api/download/${result.sessionId}`}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-lg font-semibold transition-all"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Télécharger l'APK
                </a>
                <button
                  onClick={resetForm}
                  className="block w-full mt-4 text-slate-400 hover:text-white text-sm transition-colors"
                >
                  Transformer un autre fichier
                </button>
              </div>
            ) : (
              <button
                onClick={handleUpload}
                disabled={loading || !file || !appName || !packageId}
                className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed rounded-xl font-semibold text-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-purple-500/25"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-3">
                    <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Traitement en cours...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Transformer l'APK
                  </span>
                )}
              </button>
            )}
          </div>

          <footer className="text-center mt-8 text-slate-500 text-sm">
            <p>Développé avec ♡ pour la communauté Android</p>
          </footer>
        </div>
      </div>
    </div>
  )
}