function chatLayout() {
  return {
    sidebarOpen: false,
    darkMode: localStorage.getItem('nexamind-theme') === 'dark',
    toggleTheme() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('nexamind-theme', this.darkMode ? 'dark' : 'light');
    },
  };
}
