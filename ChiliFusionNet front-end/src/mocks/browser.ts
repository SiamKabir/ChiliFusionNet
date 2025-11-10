import { setupWorker } from 'msw/browser';
// import { handlers } from './handlers';

// ❌ DISABLED: No handlers - using real backend API
export const worker = setupWorker();
