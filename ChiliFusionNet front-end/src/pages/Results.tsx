import React from 'react';

export const Results: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Results & Analysis
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            TODO: Extract key metrics from Result analysis and discussion.pdf
          </p>
          
          <div className="grid md:grid-cols-2 gap-8 mt-8">
            <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700">
              <h3 className="text-lg font-semibold mb-4">Overall Performance</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Accuracy:</span>
                  <span className="font-mono">TODO: %</span>
                </div>
                <div className="flex justify-between">
                  <span>F1 Score:</span>
                  <span className="font-mono">TODO: %</span>
                </div>
                <div className="flex justify-between">
                  <span>Precision:</span>
                  <span className="font-mono">TODO: %</span>
                </div>
                <div className="flex justify-between">
                  <span>Recall:</span>
                  <span className="font-mono">TODO: %</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700">
              <h3 className="text-lg font-semibold mb-4">Cross-Validation</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                TODO: Add cross-validation results and stability metrics
              </p>
            </div>
          </div>
          
          <div className="mt-8 space-y-6">
            <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
              <h3 className="text-lg font-semibold mb-4">Confusion Matrix</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                TODO: Add confusion matrix visualization
              </p>
            </div>
            
            <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
              <h3 className="text-lg font-semibold mb-4">ROC Curves</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                TODO: Add ROC curve visualizations
              </p>
            </div>
            
            <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
              <h3 className="text-lg font-semibold mb-4">XAI (Explainable AI)</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                TODO: Add explainability analysis and Grad-CAM examples
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
