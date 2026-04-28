import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [mode, setMode] = useState('express')
  const [file, setFile] = useState(null)
  const [appName, setAppName] = useState('')
  const [packageId, setPackageId] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleUpload = async () => {
    if (!file || !appName || !packageId) {
      alert('Veuillez remplir tous les champs')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const uploadRes = await axios.post('http://localhost:8000/api/upload', formData)
      const sessionId = uploadRes.data.session_id

      const processRes = await axios.post(`http://localhost:8000/api/process/${sessionId}`, {
        new_app_name: appName,
        new_package_id: packageId,
        mode: mode
      })

      setResult(processRes.data)
    } catch (error) {
      alert('Erreur: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">Mobile-Morpher</h1>
        
        <div className="max-w-2xl mx-auto bg-white/10 backdrop-blur rounded-xl p-6">
          <div className="flex gap-4 mb-6">
            {['express', 'design', 'developer'].map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`flex-1 py-2 rounded-lg ${mode === m ? 'bg-blue-600' : 'bg-white/20'}`}
              >
                {m.charAt(0).toUpperCase() + m.slice(1)}
              </button>
            ))}
          </div>

          <input
            type="file"
            accept=".apk"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full mb-4 p-2 rounded bg-white/20"
          />

          <input
            type="text"
            placeholder="Nouveau nom de l'app"
            value={appName}
            onChange={(e) => setAppName(e.target.value)}
            className="w-full mb-4 p-2 rounded bg-white/20 text-white"
          />

          <input
            type="text"
            placeholder="Nouveau Package ID (ex: com.monapp.pro)"
            value={packageId}
            onChange={(e) => setPackageId(e.target.value)}
            className="w-full mb-4 p-2 rounded bg-white/20 text-white"
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold"
          >
            {loading ? 'Traitement...' : 'Transformer l\'APK'}
          </button>

          {result && (
            <div className="mt-4 p-4 bg-green-600/20 rounded">
              <p>✓ Transformation réussie!</p>
              <a href={`http://localhost:8000/api/download/${result.session_id}`} 
                 className="text-blue-300 underline">Télécharger l'APK</a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
