import { http, HttpResponse } from 'msw';
import { CLASS_LABELS } from '../lib/constants';

// Mock inference response generator
const generateMockInference = (fileName: string) => {
  const randomClass = CLASS_LABELS[Math.floor(Math.random() * CLASS_LABELS.length)];
  const confidence = 0.7 + Math.random() * 0.3; // 70-100% confidence
  
  // Generate top-k results
  const topk = CLASS_LABELS.map(label => ({
    label,
    confidence: label === randomClass ? confidence : Math.random() * 0.6
  })).sort((a, b) => b.confidence - a.confidence);

  // Optional mock heatmap (base64 encoded small image)
  const mockHeatmap = Math.random() > 0.5 ? 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==' : undefined;

  return {
    model: 'ChiliFusionNet',
    timestamp: new Date().toISOString(),
    fileName,
    top1: {
      label: topk[0].label,
      confidence: topk[0].confidence
    },
    topk: topk.slice(0, 3),
    heatmap: mockHeatmap
  };
};

export const handlers = [
  // POST /api/infer - Image inference endpoint
  http.post('/api/infer', async ({ request }) => {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 2000));

    try {
      const formData = await request.formData();
      const file = formData.get('image') as File;
      
      if (!file) {
        return HttpResponse.json(
          { error: 'No image file provided' },
          { status: 400 }
        );
      }

      // Validate file type
      if (!file.type.startsWith('image/')) {
        return HttpResponse.json(
          { error: 'Invalid file type. Please upload an image.' },
          { status: 400 }
        );
      }

      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        return HttpResponse.json(
          { error: 'File too large. Maximum size is 10MB.' },
          { status: 400 }
        );
      }

      // Generate mock response
      const response = generateMockInference(file.name);
      
      return HttpResponse.json(response);
    } catch (error) {
      return HttpResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  }),

  // GET /api/examples - Get example images metadata
  http.get('/api/examples', () => {
    const examples = [
      {
        id: 1,
        name: 'bacterial_spot_example.jpg',
        url: '/examples/bacterial_spot_example.jpg',
        actualClass: 'Bacterial Spot'
      },
      {
        id: 2,
        name: 'cercospora_example.jpg',
        url: '/examples/cercospora_example.jpg',
        actualClass: 'Cercospora Leaf Spot'
      },
      {
        id: 3,
        name: 'curl_virus_example.jpg',
        url: '/examples/curl_virus_example.jpg',
        actualClass: 'Curl Virus'
      },
      {
        id: 4,
        name: 'healthy_example.jpg',
        url: '/examples/healthy_example.jpg',
        actualClass: 'Healthy Leaf'
      },
      {
        id: 5,
        name: 'nutrition_deficiency_example.jpg',
        url: '/examples/nutrition_deficiency_example.jpg',
        actualClass: 'Nutrition Deficiency'
      },
      {
        id: 6,
        name: 'white_spot_example.jpg',
        url: '/examples/white_spot_example.jpg',
        actualClass: 'White Spot'
      }
    ];

    return HttpResponse.json(examples);
  })
];
