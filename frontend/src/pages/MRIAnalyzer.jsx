import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchPatients, fetchSampleMRIs, uploadMRI, analyzeSampleMRI, BASE } from '../api'

export default function MRIAnalyzer() {
  const navigate = useNavigate()
  const [patients, setPatients] = useState([])
  const [selectedPatient, setSelectedPatient] = useState('')
  const [samples, setSamples] = useState([])
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [opacity, setOpacity] = useState(0.8)

  useEffect(() => {
    fetchPatients()
      .then(data => {
        setPatients(data)
        if (data.length > 0) setSelectedPatient(data[0].id)
      })
      .catch(err => setError(err.message))

    fetchSampleMRIs()
      .then(setSamples)
      .catch(() => {})
  }, [])

  async function handleFileUpload(e) {
    e.preventDefault()
    if (!selectedPatient) return setError('Please select a patient first.')
    if (!file) return setError('Please choose an MRI image file.')

    setLoading(true)
    setError('')
    try {
      const res = await uploadMRI(selectedPatient, file)
      setResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleSampleSelect(sampleKey) {
    if (!selectedPatient) return setError('Please select a patient first.')
    setLoading(true)
    setError('')
    try {
      const res = await analyzeSampleMRI(selectedPatient, sampleKey)
      setResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header-flex">
        <div>
          <h1>🧠 MRI Brain Scan Analyzer & Deep Learning Staging</h1>
          <p className="subtitle">
            Powered by PyTorch Convolutional Neural Network trained on Augmented Alzheimer MRI Dataset (4 Staging Classes)
          </p>
        </div>
      </div>

      <div className="card shadow-glow">
        <h3>1. Select Patient & MRI Input Method</h3>
        {error && <div className="error-alert">{error}</div>}

        <div className="form-group" style={{ marginBottom: 20 }}>
          <label>Target Patient:</label>
          <select 
            value={selectedPatient} 
            onChange={(e) => setSelectedPatient(e.target.value)}
            className="input-select"
          >
            {patients.map(p => (
              <option key={p.id} value={p.id}>
                {p.full_name} (Age: {p.age}, Gender: {p.gender})
              </option>
            ))}
          </select>
        </div>

        <div className="mri-grid">
          {/* Custom File Upload Box */}
          <div className="upload-box">
            <h4>Upload Custom Scan (DICOM / PNG / JPG)</h4>
            <form onSubmit={handleFileUpload}>
              <input 
                type="file" 
                accept=".dcm,.dicom,.png,.jpg,.jpeg" 
                onChange={(e) => setFile(e.target.files[0])}
                className="file-input"
              />
              <button 
                type="submit" 
                disabled={loading || !file} 
                className="btn btn-primary btn-full"
              >
                {loading ? 'Analyzing Scan with PyTorch DL...' : 'Upload & Analyze MRI'}
              </button>
            </form>
          </div>

          {/* Preset Samples */}
          <div className="samples-box">
            <h4>Quick Test: Kaggle MRI Dataset Samples</h4>
            <div className="sample-buttons">
              {samples.map(s => (
                <button
                  key={s.key}
                  onClick={() => handleSampleSelect(s.key)}
                  disabled={loading}
                  className="btn btn-sample"
                >
                  <span className="sample-icon">🔬</span>
                  <span>{s.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {loading && (
        <div className="card loading-card">
          <div className="spinner"></div>
          <p>Running Neural Network Inference & Extracting SHAP Atrophy Heatmap...</p>
        </div>
      )}

      {result && !loading && (
        <div className="card shadow-glow animate-fade-in">
          <div className="result-header">
            <div>
              <h2>MRI Deep Learning Diagnosis</h2>
              <p>Scan File: <strong>{result.filename}</strong></p>
            </div>
            <div className="stage-banner">
              <span className={`badge stage-${result.predicted_stage.replace(/\s+/g, '-').toLowerCase()}`}>
                {result.predicted_stage}
              </span>
              <span className="confidence-pill">
                {result.confidence_score}% Confidence
              </span>
            </div>
          </div>

          {/* Side-by-side Original vs SHAP Heatmap */}
          <div className="mri-visualizer-container">
            <div className="visualizer-card">
              <h4>Original Grayscale MRI Scan</h4>
              <div className="img-wrapper">
                <img src={`${BASE}${result.original_url}`} alt="Original MRI" />
              </div>
            </div>

            <div className="visualizer-card">
              <h4>SHAP / Grad-CAM Visual Heatmap (Brain Atrophy)</h4>
              <div className="img-wrapper relative">
                <img src={`${BASE}${result.original_url}`} alt="Original Background" className="bg-img" />
                <img 
                  src={`${BASE}${result.heatmap_url}`} 
                  alt="SHAP Overlay" 
                  className="overlay-img" 
                  style={{ opacity: opacity }}
                />
              </div>
              <div className="slider-control">
                <label>Heatmap Opacity ({Math.round(opacity * 100)}%):</label>
                <input 
                  type="range" 
                  min="0" 
                  max="1" 
                  step="0.05" 
                  value={opacity} 
                  onChange={(e) => setOpacity(parseFloat(e.target.value))}
                />
              </div>
            </div>
          </div>

          {/* Staging Class Probabilities */}
          <div className="probabilities-section">
            <h4>4-Class Alzheimer MRI Dataset Probability Distribution</h4>
            <div className="prob-bars">
              {Object.entries(result.stage_probabilities || {}).map(([stage, prob]) => {
                const percent = Math.round(prob * 100)
                return (
                  <div key={stage} className="prob-row">
                    <div className="prob-label">
                      <span>{stage}</span>
                      <span>{percent}%</span>
                    </div>
                    <div className="progress-track">
                      <div 
                        className={`progress-fill ${stage === result.predicted_stage ? 'active' : ''}`}
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="action-footer">
            <button 
              onClick={() => navigate(`/patients/${selectedPatient}/assess?mri_id=${result.id}`)}
              className="btn btn-success btn-lg"
            >
              📋 Proceed to Full Cognitive Assessment with this MRI
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
