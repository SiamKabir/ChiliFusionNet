import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-900">
      <div className="container-width section-padding py-8">
        <div className="text-center text-sm text-neutral-600 dark:text-neutral-400">
          <p className="mb-2">
            © 2025 ChiliFusionNet Research Team. Built for academic research purposes.
          </p>
          <p>
            {/* Research based on IEX-FeatureNet and ensemble learning methodologies. */}
          </p>
        </div>
      </div>
    </footer>
  );
};
