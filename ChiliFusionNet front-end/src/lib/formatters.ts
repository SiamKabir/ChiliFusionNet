export const formatConfidence = (confidence: number): string => {
  return `${(confidence * 100).toFixed(1)}%`;
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const formatTimestamp = (timestamp: string): string => {
  return new Date(timestamp).toLocaleString();
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

export const getClassColor = (className: string): string => {
  const colors = {
    'Bacterial Spot': 'bg-red-500',
    'Cercospora Leaf Spot': 'bg-orange-500',
    'Curl Virus': 'bg-yellow-500',
    'Healthy Leaf': 'bg-green-500',
    'Nutrition Deficiency': 'bg-purple-500',
    'White Spot': 'bg-blue-500',
  };
  
  return colors[className as keyof typeof colors] || 'bg-gray-500';
};
