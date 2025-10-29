import React from 'react';
import { CLASS_LABELS } from '../lib/constants';

export const Dataset: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Dataset Information
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-8">
            TODO: Extract dataset details from introduction chili.pdf
          </p>
          
          <h2 className="text-2xl font-bold mb-6">Disease Classes</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {CLASS_LABELS.map((className, index) => (
              <div 
                key={className}
                className="bg-white dark:bg-neutral-800 p-6 rounded-xl border border-neutral-200 dark:border-neutral-700"
              >
                <div className="flex items-center space-x-3 mb-3">
                  <div className={`w-4 h-4 rounded-full bg-primary-${(index + 1) * 100}`}></div>
                  <h3 className="font-semibold">{className}</h3>
                </div>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  TODO: Add class description and sample count
                </p>
              </div>
            ))}
          </div>
          
          <div className="mt-12 grid md:grid-cols-2 gap-8">
            <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
              <h3 className="text-lg font-semibold mb-4">Collection Information</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li>Total Images: TODO</li>
                <li>Image Resolution: TODO</li>
                <li>Collection Period: TODO</li>
                <li>Geographic Location: TODO</li>
                <li>Camera Equipment: TODO</li>
              </ul>
            </div>
            
            <div className="bg-neutral-100 dark:bg-neutral-800 p-6 rounded-xl">
              <h3 className="text-lg font-semibold mb-4">Data Split</h3>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li>Training Set: TODO %</li>
                <li>Validation Set: TODO %</li>
                <li>Test Set: TODO %</li>
                <li>Cross-validation: TODO folds</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
