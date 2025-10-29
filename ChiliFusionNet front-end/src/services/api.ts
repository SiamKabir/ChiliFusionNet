const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export interface PredictionResult {
  predicted_label: string;
  confidence: number;
  probabilities?: Record<string, number>;
}

export const predictImage = async (file: File): Promise<PredictionResult> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Prediction failed');
  }

  return response.json();
};
