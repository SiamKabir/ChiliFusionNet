import classLabelsData from './classLabels.json';

export const CLASS_LABELS = classLabelsData as readonly string[];
export type ClassLabel = typeof CLASS_LABELS[number];

export const MODEL_NAME = 'ChiliFusionNet';

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ACCEPTED_IMAGE_TYPES = [
  'image/jpeg',
  'image/jpg', 
  'image/png'
] as const;

export const CONFIDENCE_THRESHOLD = 0.5;
export const TOP_K_RESULTS = 3;

export const DATASET_INFO = {
  totalImages: 'TODO: Add total image count',
  classes: CLASS_LABELS.length,
  splitRatio: 'TODO: Add train/val/test split',
  augmentation: 'TODO: Add augmentation details'
};

export const MODEL_METRICS = {
  accuracy: 'TODO: Add overall accuracy',
  f1Score: 'TODO: Add F1 score',
  precision: 'TODO: Add precision',
  recall: 'TODO: Add recall'
};

export const SAMPLE_METRICS = {
  accuracy: 0.95,
  perClassF1: [
    { class: 'Bacterial Spot', f1: 0.92 },
    { class: 'Cercospora Leaf Spot', f1: 0.94 },
    { class: 'Curl Virus', f1: 0.88 },
    { class: 'Healthy Leaf', f1: 0.98 },
    { class: 'Nutrition Deficiency', f1: 0.90 },
    { class: 'White Spot', f1: 0.93 }
  ],
  trainingCurve: [
    { epoch: 1, train: 0.75, val: 0.72 },
    { epoch: 2, train: 0.82, val: 0.79 },
    { epoch: 3, train: 0.88, val: 0.85 },
    { epoch: 4, train: 0.92, val: 0.89 },
    { epoch: 5, train: 0.95, val: 0.92 }
  ]
};
