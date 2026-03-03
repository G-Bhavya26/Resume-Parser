import React, { useState, useCallback } from 'react'
import {
  Upload,
  FileText,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Zap,
  ShieldCheck,
  Cpu,
  Briefcase,
  Terminal,
  ChevronRight
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import './App.css'

interface ParseResponse {
  resume_id: string;
  student_name: string;
  email: string;
  phone: string;
  parse_status: string;
  parse_confidence: number;
  skills: Array<{ name: string; confidence: number }>;
  projects: Array<{ title: string; description: string; confidence: number }>;
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ParseResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const uploadResume = async () => {
    if (!file) return;

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      // API call to the backend
      const response = await axios.post('http://localhost:8000/api/v1/parse', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong during parsing.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* Header / Hero */}
      <header className="hero-section">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="float-animation" style={{ display: 'inline-block', marginBottom: '1.5rem' }}>
            <div className="glass-card" style={{ padding: '16px', borderRadius: '50%', background: 'rgba(225,6,0,0.1)' }}>
              <Cpu className="title-gradient" size={48} />
            </div>
          </div>
          <h1 className="hero-title title-gradient">CRMS Intelligence</h1>
          <p className="hero-subtitle">
            Advanced Resume Extraction and Semantic Matching using Finetuned
            <span style={{ color: 'var(--primary)', fontWeight: 700 }}> DistilBERT </span>
            and <span style={{ color: 'var(--text-main)', fontWeight: 700 }}> Sentence-BERT </span>
          </p>
        </motion.div>
      </header>

      {/* Main Action Area */}
      <main>
        <AnimatePresence>
          {!result && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-card upload-card"
            >
              <div
                className={`upload-zone ${dragActive ? 'active' : ''}`}
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <input
                  id="file-input"
                  type="file"
                  accept=".pdf"
                  className="hidden-input"
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />

                <Upload size={48} className="text-dim mb-4" />
                <h3 style={{ margin: '15px 0' }}>{file ? file.name : 'Drop your Resume PDF here'}</h3>
                <p className="text-dim">or click to browse your files (Max 5MB)</p>
              </div>

              {file && (
                <div style={{ marginTop: '30px' }}>
                  <button
                    className="btn btn-primary"
                    style={{ width: '100%', justifyContent: 'center', height: '50px' }}
                    onClick={uploadResume}
                    disabled={loading}
                  >
                    {loading ? (
                      <Loader2 className="animate-spin" />
                    ) : (
                      <>
                        <Zap size={20} />
                        Analyze Resume
                      </>
                    )}
                  </button>
                </div>
              )}

              {error && (
                <div style={{ color: 'var(--error)', marginTop: '20px', display: 'flex', gap: '8px', justifyContent: 'center' }}>
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              )}
            </motion.div>
          )}

          {result && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-card result-card"
            >
              <div className="section-title">
                <CheckCircle2 color="var(--success)" />
                <span>Parsing Result for: <span className="title-gradient">{result.student_name}</span></span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
                {/* Profile Meta */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div className="text-dim mb-4 flex items-center gap-2">
                    <ShieldCheck size={16} />
                    <span>Metadata</span>
                  </div>
                  <div style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
                    <div>Confidence: {(result.parse_confidence * 100).toFixed(1)}%</div>
                    <div>Email: {result.email}</div>
                    <div>Phone: {result.phone}</div>
                  </div>
                </div>

                {/* Skills */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div className="section-title" style={{ fontSize: '1.1rem', marginBottom: '15px' }}>
                    <Terminal size={18} />
                    <span>Skills</span>
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {result.skills.map((skill, i) => (
                      <span key={i} className="skill-tag">
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Projects */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div className="section-title" style={{ fontSize: '1.1rem', marginBottom: '15px' }}>
                    <Briefcase size={18} />
                    <span>Key Projects</span>
                  </div>
                  {result.projects.map((proj, i) => (
                    <div key={i} className="project-item">
                      <strong>{proj.title}</strong>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                        {proj.description.substring(0, 100)}...
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ marginTop: '30px', textAlign: 'center' }}>
                <button className="btn" onClick={() => setResult(null)}>
                  Upload another resume <ChevronRight size={18} />
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer style={{ marginTop: '80px', textAlign: 'center', opacity: 0.5, fontSize: '0.8rem' }}>
        &copy; 2026 CRMS Intelligent Resume Parsing Service v1.0
      </footer>
    </div>
  )
}

export default App
