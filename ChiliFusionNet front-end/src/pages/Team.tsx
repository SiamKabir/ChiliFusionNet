import React from 'react';

export const Team: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Authors
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-12">
          Meet the research team behind ChiliFusionNet
        </p>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {/* Author 1 */}
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700 text-center">
            <div className="w-20 h-20 mx-auto mb-4 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
              <span className="text-2xl">👤</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Dr. [Principal Investigator]</h3>
            <p className="text-primary-600 dark:text-primary-400 mb-2">Principal Investigator</p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
              [University/Institution Name]
            </p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Lead researcher specializing in deep learning applications for agricultural technology.
            </p>
          </div>

          {/* Author 2 */}
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700 text-center">
            <div className="w-20 h-20 mx-auto mb-4 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
              <span className="text-2xl">�</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">[Co-Author Name]</h3>
            <p className="text-primary-600 dark:text-primary-400 mb-2">Co-Author</p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
              [University/Institution Name]
            </p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Computer vision researcher with expertise in plant pathology.
            </p>
          </div>

          {/* Author 3 */}
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700 text-center">
            <div className="w-20 h-20 mx-auto mb-4 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
              <span className="text-2xl">👤</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">[Co-Author Name]</h3>
            <p className="text-primary-600 dark:text-primary-400 mb-2">Co-Author</p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-3">
              [University/Institution Name]
            </p>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Machine learning specialist focusing on ensemble methods.
            </p>
          </div>
        </div>

        <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
          <h3 className="text-lg font-semibold mb-4">Research Contributions</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium mb-2">Methodology Development</h4>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Design and implementation of the ChiliFusionNet ensemble architecture
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Data Collection & Analysis</h4>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Comprehensive dataset curation and experimental validation
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Model Optimization</h4>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Performance tuning and comparative analysis with state-of-the-art methods
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Publication & Documentation</h4>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Research documentation and manuscript preparation
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const References: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          References
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-8">
            Research citations and bibliography
          </p>
          
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700">
            <h3 className="text-lg font-semibold mb-4">Primary Research Papers</h3>
            <div className="space-y-4">
              <div className="border-l-4 border-primary-500 pl-4">
                <p className="font-medium">Introduction to Chili Disease Detection</p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  Source: introduction chili.pdf
                </p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  TODO: Add proper citation format
                </p>
              </div>
              
              <div className="border-l-4 border-primary-500 pl-4">
                <p className="font-medium">Result Analysis and Discussion</p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  Source: Result analysis and discussion.pdf
                </p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  TODO: Add proper citation format
                </p>
              </div>
            </div>
          </div>
          
          <div className="mt-8 bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
            <h3 className="text-lg font-semibold mb-4">Additional References</h3>
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              TODO: Add bibliography for related work in machine learning, 
              computer vision, and plant disease detection
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export const NotFound: React.FC = () => {
  return (
    <div className="section-padding text-center">
      <div className="container-width">
        <div className="w-24 h-24 mx-auto mb-6 bg-accent-100 dark:bg-accent-900 rounded-full flex items-center justify-center">
          <span className="text-3xl">🔍</span>
        </div>
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">
          404 - Page Not Found
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <a 
          href="/" 
          className="btn-primary"
        >
          Return Home
        </a>
      </div>
    </div>
  );
};
