export function registerNavConfig(up) {
    if (!up.feedback.config.currentClasses.includes('is-active')) {
        up.feedback.config.currentClasses.push('is-active');
    }
}

if (typeof window !== 'undefined' && window.up) {
    registerNavConfig(window.up);
}