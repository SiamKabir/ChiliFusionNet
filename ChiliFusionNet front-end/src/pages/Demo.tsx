import React, { useState, useRef } from 'react';
import { predictImage } from '../services/api';
import type { PredictionResult } from '../services/api';
import ExampleImages, { ExampleSelection } from '../components/ExampleImages';

export const Demo: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setPrediction(null);
      setError(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setPrediction(null);
      setError(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleSubmit = async (e?: React.MouseEvent) => {
    // Prevent any default behavior
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    // Validate that user has selected something
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    console.log('🚀 Submit clicked!');
    console.log('Selected image:', selectedImage);

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      console.log('📤 Uploading file to /predict...');
      const result = await predictImage(selectedImage);
      
      console.log('✅ Prediction result:', result);
      setPrediction(result);
    } catch (err) {
      console.error('❌ Prediction error:', err);
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (selection: ExampleSelection) => {
    console.log('🖼️ Example clicked:', selection.label);
    setPreview(selection.previewUrl);
    setSelectedImage(selection.file);
    setPrediction(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    console.log('✅ Example loaded, ready to submit');
  };

  const handleClear = () => {
    setSelectedImage(null);
    setPreview(null);
    setPrediction(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Interactive Demo
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-12">
          Upload a chili leaf image to get instant disease classification with confidence scores.
        </p>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Left Column - Upload & Controls */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-6">
              {/* Upload Area */}
              <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
                  preview 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
                    : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-500 dark:hover:border-primary-500'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => !preview && fileInputRef.current?.click()}
              >
                {!preview ? (
                  <div className="space-y-4">
                    <div className="w-16 h-16 mx-auto bg-neutral-100 dark:bg-neutral-700 rounded-full flex items-center justify-center">
                      <svg className="w-8 h-8 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100">Drop Image Here</h3>
                      <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">or</p>
                      <button 
                        className="mt-3 px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
                        onClick={(e) => {
                          e.stopPropagation();
                          fileInputRef.current?.click();
                        }}
                      >
                        Click to Upload
                      </button>
                    </div>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                      className="hidden"
                    />
                  </div>
                ) : (
                  <div className="relative">
                    <img 
                      src={preview} 
                      alt="Preview" 
                      className="max-h-80 mx-auto rounded-lg shadow-lg"
                    />
                    <button
                      className="absolute top-2 right-2 p-2 bg-red-500 hover:bg-red-600 text-white rounded-full transition-colors shadow-lg"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleClear();
                      }}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>


              {/* Action Buttons */}
              <div className="mt-6 flex gap-3">
                <button
                  type="button"
                  onClick={handleClear}
                  className="flex-1 px-6 py-3 bg-neutral-200 hover:bg-neutral-300 dark:bg-neutral-700 dark:hover:bg-neutral-600 text-neutral-900 dark:text-neutral-100 font-medium rounded-lg transition-colors"
                >
                  Clear
                </button>
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={!selectedImage || loading}
                  className="flex-1 px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-neutral-300 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    'Submit'
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-6">
            <h3 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-6">
              Classification Results
            </h3>

            {loading && (
              <div className="text-center py-12">
                <div className="w-16 h-16 mx-auto mb-4 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-neutral-600 dark:text-neutral-400">Analyzing image...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start gap-3">
                <svg className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="font-medium text-red-900 dark:text-red-100">Error</p>
                  <p className="text-sm text-red-700 dark:text-red-300 mt-1">{error}</p>
                </div>
              </div>
            )}

            {prediction && (
              <div className="space-y-6">
                <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 rounded-xl p-6 border border-primary-200 dark:border-primary-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-primary-700 dark:text-primary-300">Predicted Class</span>
                    <span className="text-sm font-medium text-primary-700 dark:text-primary-300">Confidence</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <h4 className="text-2xl font-bold text-primary-900 dark:text-primary-100">
                      {prediction.predicted_label}
                    </h4>
                    <span className="text-3xl font-bold text-primary-900 dark:text-primary-100">
                      {(prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="mt-4 h-3 bg-white/50 dark:bg-black/30 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-600 dark:bg-primary-500 rounded-full transition-all duration-500"
                      style={{ width: `${prediction.confidence * 100}%` }}
                    ></div>
                  </div>
                </div>

                {prediction.probabilities && (
                  <div className="bg-neutral-50 dark:bg-neutral-900/40 rounded-xl border border-neutral-200 dark:border-neutral-700 p-6">
                    <h4 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">Class Probabilities</h4>
                    <div className="space-y-4">
                      {Object.entries(prediction.probabilities)
                        .sort((a, b) => b[1] - a[1])
                        .map(([label, prob]) => (
                          <div key={label} className="space-y-1">
                            <div className="flex items-center justify-between text-sm">
                              <span className="font-medium text-neutral-700 dark:text-neutral-200">{label}</span>
                              <span className="font-semibold text-neutral-900 dark:text-neutral-100">{(prob * 100).toFixed(2)}%</span>
                            </div>
                            <div className="h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-primary-500 dark:bg-primary-400 transition-all duration-500"
                                style={{ width: `${Math.min(Math.max(prob * 100, prob > 0 ? 2 : 0), 100)}%` }}
                              ></div>
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {!loading && !prediction && !error && (
              <div className="text-center py-12">
                <div className="w-16 h-16 mx-auto mb-4 bg-neutral-100 dark:bg-neutral-700 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <p className="text-neutral-500 dark:text-neutral-400">
                  Upload an image to see classification results
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Examples Section */}
        <ExampleImages onExampleSelect={handleExampleClick} />
      </div>
    </div>
  );
};