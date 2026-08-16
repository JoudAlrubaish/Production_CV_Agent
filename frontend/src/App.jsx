import { useEffect, useState } from "react";
import "./App.css";


const API_BASE_URL = "http://localhost:8020";


function App() {
  // Selected image
  const [selectedImage, setSelectedImage] = useState(null);

  // Image preview
  const [previewUrl, setPreviewUrl] = useState(null);

  // Current prediction result
  const [prediction, setPrediction] = useState(null);

  // Prediction loading state
  const [loading, setLoading] = useState(false);

  // Prediction error
  const [error, setError] = useState("");

  // Statistics from PostgreSQL
  const [stats, setStats] = useState({
    total_predictions: 0,
    class_distribution: {},
    average_confidence: 0,
  });

  // Prediction history
  const [history, setHistory] = useState([]);

  // Dashboard loading state
  const [dashboardLoading, setDashboardLoading] = useState(true);

  // Dashboard error
  const [dashboardError, setDashboardError] = useState("");


  // Load statistics + prediction history
  async function loadDashboardData() {
    setDashboardLoading(true);
    setDashboardError("");

    try {
      const [statsResponse, historyResponse] =
        await Promise.all([
          fetch(`${API_BASE_URL}/api/v1/stats`),
          fetch(`${API_BASE_URL}/api/v1/predictions`),
        ]);

      if (!statsResponse.ok || !historyResponse.ok) {
        throw new Error(
          "Unable to load dashboard data."
        );
      }

      const statsData = await statsResponse.json();
      const historyData = await historyResponse.json();

      setStats(statsData);
      setHistory(historyData);

    } catch (err) {
      setDashboardError(err.message);

    } finally {
      setDashboardLoading(false);
    }
  }


// Load dashboard data once when the page opens
useEffect(() => {
  async function loadInitialDashboardData() {
    try {
      const [statsResponse, historyResponse] =
        await Promise.all([
          fetch(`${API_BASE_URL}/api/v1/stats`),
          fetch(`${API_BASE_URL}/api/v1/predictions`),
        ]);

      if (!statsResponse.ok || !historyResponse.ok) {
        throw new Error(
          "Unable to load dashboard data."
        );
      }

      const statsData = await statsResponse.json();
      const historyData = await historyResponse.json();

      setStats(statsData);
      setHistory(historyData);

    } catch (err) {
      setDashboardError(err.message);

    } finally {
      setDashboardLoading(false);
    }
  }

  loadInitialDashboardData();
}, []);

  // Runs when user chooses an image
  function handleImageChange(event) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedImage(file);

    const imageUrl =
      URL.createObjectURL(file);

    setPreviewUrl(imageUrl);

    // Clear old prediction
    setPrediction(null);
    setError("");
  }


  // Send image to FastAPI
  async function handleAnalyze() {
    if (!selectedImage) {
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    const formData = new FormData();

    formData.append(
      "image",
      selectedImage
    );

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/predict`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Prediction failed."
        );
      }

      // Show result
      setPrediction(data);

      // Refresh dashboard because a new
      // prediction was stored in PostgreSQL
      await loadDashboardData();

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="app">

      <main className="main-content">

        {/* Hero */}
        <section className="hero">

          <div className="system-name">
            EmotionAI
          </div>

          <div className="hero-badge">
            AI-Powered Computer Vision
          </div>

          <h1>
            Understand facial emotion
            <span> with AI.</span>
          </h1>

          <p>
            Upload a facial image and let our
            computer vision model analyze the
            expression in seconds.
          </p>

        </section>


        {/* Upload + Preview */}
        <section className="workspace">

          {/* Upload */}
          <div className="panel upload-panel">

            <div className="panel-header">

              <div>
                <span className="step-number">
                  01
                </span>

                <h3>
                  Upload Image
                </h3>
              </div>

              <p>
                Select a clear image containing
                a face.
              </p>

            </div>


            <label
              htmlFor="image-upload"
              className="upload-zone"
            >

              <div className="upload-icon">
                ↑
              </div>

              <h4>
                {selectedImage
                  ? "Choose another image"
                  : "Choose an image"}
              </h4>

              <p>
                Click here to browse your files
              </p>

              <div className="file-types">
                <span>JPG</span>
                <span>PNG</span>
                <span>WEBP</span>
                <span>Max 5 MB</span>
              </div>

            </label>


            <input
              id="image-upload"
              className="file-input"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={handleImageChange}
            />


            {selectedImage && (

              <div className="selected-file">

                <div className="file-icon">
                  IMG
                </div>

                <div className="file-details">

                  <strong>
                    {selectedImage.name}
                  </strong>

                  <span>
                    {(selectedImage.size / 1024)
                      .toFixed(1)} KB
                  </span>

                </div>

                <span className="file-success">
                  ✓
                </span>

              </div>

            )}

          </div>


          {/* Preview */}
          <div className="panel preview-panel">

            <div className="panel-header">

              <div>
                <span className="step-number">
                  02
                </span>

                <h3>
                  Image Preview
                </h3>
              </div>

              <p>
                Review the image before analysis.
              </p>

            </div>


            <div className="preview-container">

              {previewUrl ? (

                <img
                  src={previewUrl}
                  alt="Selected preview"
                  className="image-preview"
                />

              ) : (

                <div className="empty-preview">

                  <div className="empty-icon">
                    ◫
                  </div>

                  <h4>
                    No image selected
                  </h4>

                  <p>
                    Your image preview will
                    appear here.
                  </p>

                </div>

              )}

            </div>

          </div>

        </section>


        {/* Analyze */}
        <div className="action-area">

          <button
            className="analyze-button"
            disabled={
              !selectedImage ||
              loading
            }
            type="button"
            onClick={handleAnalyze}
          >

            {loading
              ? "Analyzing..."
              : "Analyze Emotion"}

            {!loading && (
              <span>→</span>
            )}

          </button>

          <p>
            The image is processed through
            the computer vision prediction API.
          </p>

        </div>


        {/* Prediction error */}
        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        {/* Prediction result */}
        {prediction && (

          <section className="result-card">

            <div className="result-header">

              <div>

                <span className="result-label">
                  Prediction Result
                </span>

                <h2>
                  {prediction.predicted_class}
                </h2>

              </div>


              <div className="confidence-box">

                <span>
                  Confidence
                </span>

                <strong>
                  {(prediction.confidence * 100)
                    .toFixed(1)}%
                </strong>

              </div>

            </div>


            {/* Top K */}
            <div className="top-predictions">

              <h3>
                Top Predictions
              </h3>

              {prediction.top_k_predictions.map(
                (item) => (

                  <div
                    className="prediction-row"
                    key={item.class_name}
                  >

                    <div className="prediction-name">

                      <span>
                        {item.class_name}
                      </span>

                      <strong>
                        {(item.probability * 100)
                          .toFixed(1)}%
                      </strong>

                    </div>


                    <div className="progress-track">

                      <div
                        className="progress-value"
                        style={{
                          width:
                            `${item.probability * 100}%`,
                        }}
                      />

                    </div>

                  </div>

                )
              )}

            </div>


            {/* Metadata */}
            <div className="result-meta">

              <div>
                <span>
                  Inference Time
                </span>

                <strong>
                  {prediction.inference_ms} ms
                </strong>
              </div>


              <div>
                <span>
                  Model Version
                </span>

                <strong>
                  v{prediction.model_version}
                </strong>
              </div>


              <div>
                <span>
                  Prediction ID
                </span>

                <strong>
                  #{prediction.id}
                </strong>
              </div>

            </div>

          </section>

        )}


        {/* ==========================
            Statistics Dashboard
        =========================== */}
        <section className="dashboard-section">

          <div className="section-heading">

            <div>
              <span className="section-label">
                Analytics
              </span>

              <h2>
                Prediction Statistics
              </h2>
            </div>

            <p>
              Live statistics calculated from
              stored predictions.
            </p>

          </div>


          {dashboardLoading ? (

            <div className="dashboard-message">
              Loading statistics...
            </div>

          ) : dashboardError ? (

            <div className="error-message">
              {dashboardError}
            </div>

          ) : (

            <>
              <div className="stats-grid">

                <div className="stat-card">

                  <span>
                    Total Predictions
                  </span>

                  <strong>
                    {stats.total_predictions}
                  </strong>

                  <p>
                    Stored classifications
                  </p>

                </div>


                <div className="stat-card">

                  <span>
                    Average Confidence
                  </span>

                  <strong>
                    {(stats.average_confidence * 100)
                      .toFixed(1)}%
                  </strong>

                  <p>
                    Across all predictions
                  </p>

                </div>


                <div className="stat-card">

                  <span>
                    Predicted Classes
                  </span>

                  <strong>
                    {
                      Object.keys(
                        stats.class_distribution
                      ).length
                    }
                  </strong>

                  <p>
                    Classes observed so far
                  </p>

                </div>

              </div>


              {/* Class distribution */}
              <div className="distribution-card">

                <h3>
                  Class Distribution
                </h3>

                {Object.keys(
                  stats.class_distribution
                ).length === 0 ? (

                  <p className="empty-data">
                    No predictions available yet.
                  </p>

                ) : (

                  <div className="distribution-list">

                    {Object.entries(
                      stats.class_distribution
                    ).map(
                      ([className, count]) => {

                        const percentage =
                          stats.total_predictions > 0
                            ? (
                                count /
                                stats.total_predictions
                              ) * 100
                            : 0;

                        return (
                          <div
                            className="distribution-row"
                            key={className}
                          >

                            <div className="distribution-info">

                              <span>
                                {className}
                              </span>

                              <strong>
                                {count}
                              </strong>

                            </div>


                            <div className="progress-track">

                              <div
                                className="progress-value"
                                style={{
                                  width:
                                    `${percentage}%`,
                                }}
                              />

                            </div>

                          </div>
                        );
                      }
                    )}

                  </div>

                )}

              </div>

            </>

          )}

        </section>


        {/* ==========================
            Prediction History
        =========================== */}
        <section className="history-section">

          <div className="section-heading">

            <div>
              <span className="section-label">
                Database
              </span>

              <h2>
                Recent Predictions
              </h2>
            </div>

            <p>
              Latest predictions stored
              in PostgreSQL.
            </p>

          </div>


          {dashboardLoading ? (

            <div className="dashboard-message">
              Loading prediction history...
            </div>

          ) : history.length === 0 ? (

            <div className="history-empty">
              No prediction history yet.
            </div>

          ) : (

            <div className="history-table-wrapper">

              <table className="history-table">

                <thead>

                  <tr>
                    <th>ID</th>
                    <th>Image</th>
                    <th>Emotion</th>
                    <th>Confidence</th>
                    <th>Inference</th>
                    <th>Date</th>
                  </tr>

                </thead>


                <tbody>

                  {history
                    .slice(0, 5)
                    .map((item) => (

                      <tr key={item.id}>

                        <td>
                          #{item.id}
                        </td>

                        <td>
                          {item.image_name}
                        </td>

                        <td>

                          <span className="emotion-badge">
                            {item.predicted_class}
                          </span>

                        </td>

                        <td>
                          {(item.confidence * 100)
                            .toFixed(1)}%
                        </td>

                        <td>
                          {item.inference_ms} ms
                        </td>

                        <td>
                          {new Date(
                            item.created_at
                          ).toLocaleString()}
                        </td>

                      </tr>

                    ))}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* System Info */}
        <section className="system-info">

          <div>
            <span>
              Model
            </span>

            <strong>
              MobileNetV3
            </strong>
          </div>


          <div>
            <span>
              Task
            </span>

            <strong>
              Emotion Classification
            </strong>
          </div>


          <div>
            <span>
              Supported Classes
            </span>

            <strong>
              6 Emotions
            </strong>
          </div>

        </section>

      </main>

    </div>
  );
}


export default App;