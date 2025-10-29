import { useState } from 'react';

export interface ExampleSelection {
  file: File;
  previewUrl: string;
  label: string;
}

interface ExampleImagesProps {
  onExampleSelect: (selection: ExampleSelection) => void;
}

const SAMPLE_IMAGES: Array<{
  filename: string;
  label: string;
  publicPath: string;
}> = [
  {
    filename: 'Healthy Leaf00110.JPG',
    label: 'Healthy Leaf',
    publicPath: '/sample images/Healthy Leaf00110.JPG',
  },
  {
    filename: 'Healthy Leaf00040.JPG',
    label: 'Healthy Leaf',
    publicPath: '/sample images/Healthy Leaf00040.JPG',
  },
  {
    filename: 'Bacterial Spot00001_bright_3.jpg',
    label: 'Bacterial Spot',
    publicPath: '/sample images/Bacterial Spot00001_bright_3.jpg',
  },
  {
    filename: 'Cercospora Leaf Spot00039.JPG',
    label: 'Cercospora Leaf Spot',
    publicPath: '/sample images/Cercospora Leaf Spot00039.JPG',
  },
  {
    filename: 'Cercospora Leaf Spot00153.JPG',
    label: 'Cercospora Leaf Spot',
    publicPath: '/sample images/Cercospora Leaf Spot00153.JPG',
  },
  {
    filename: 'Curl Virus00014.JPG',
    label: 'Curl Virus',
    publicPath: '/sample images/Curl Virus00014.JPG',
  },
  {
    filename: 'Nutrition Deficiency00003_zoomed_1518.jpg',
    label: 'Nutrition Deficiency',
    publicPath: '/sample images/Nutrition Deficiency00003_zoomed_1518.jpg',
  },
  {
    filename: 'White spot00002_rotated_7.jpg',
    label: 'White Spot',
    publicPath: '/sample images/White spot00002_rotated_7.jpg',
  },
];

const ExampleImages: React.FC<ExampleImagesProps> = ({ onExampleSelect }) => {
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSelect = async (image: (typeof SAMPLE_IMAGES)[number]) => {
    try {
      setError(null);
      setLoadingId(image.publicPath);

      const response = await fetch(image.publicPath);
      if (!response.ok) {
        throw new Error(`Failed to load ${image.filename}`);
      }

      const blob = await response.blob();
      const file = new File([blob], image.filename, { type: blob.type || 'image/jpeg' });

      onExampleSelect({
        file,
        previewUrl: image.publicPath,
        label: image.label,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load image');
    } finally {
      setLoadingId(null);
    }
  };

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100 flex items-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Examples
        </h3>
        {error && (
          <span className="text-sm text-red-600 dark:text-red-400">{error}</span>
        )}
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        {SAMPLE_IMAGES.map((image) => (
          <button
            key={image.publicPath}
            onClick={() => handleSelect(image)}
            className="group relative aspect-square rounded-lg overflow-hidden border-2 border-neutral-200 dark:border-neutral-700 hover:border-primary-500 dark:hover:border-primary-500 transition-all hover:shadow-lg"
            disabled={loadingId === image.publicPath}
          >
            <img
              src={image.publicPath}
              alt={image.filename}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/50 transition-colors flex items-end p-2">
              <p className="text-xs text-white font-medium opacity-0 group-hover:opacity-100 transition-opacity truncate">
                {image.label}
              </p>
            </div>
            {loadingId === image.publicPath && (
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ExampleImages;
