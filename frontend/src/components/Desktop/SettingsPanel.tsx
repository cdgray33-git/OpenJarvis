import { useState, useEffect } from 'react';
import type React from 'react';
import { useAppStore } from '../../lib/store';

const styles: Record<string, React.CSSProperties> = {
  container: { backgroundColor: '#1e1e2e', color: '#cdd6f4', padding: 24, maxWidth: 600 },
  heading: { fontSize: 20, fontWeight: 600, marginBottom: 24, color: '#89b4fa' },
  fieldGroup: { marginBottom: 20 },
  label: { display: 'block', fontSize: 13, fontWeight: 500, color: '#a6adc8', marginBottom: 6 },
  input: { width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #313244', backgroundColor: '#181825', color: '#cdd6f4', fontSize: 14, outline: 'none', boxSizing: 'border-box' as const },
  toggleRow: { display: 'flex', gap: 8 },
  toggleButton: { padding: '8px 16px', borderRadius: 6, border: '1px solid #313244', backgroundColor: 'transparent', color: '#a6adc8', cursor: 'pointer', fontSize: 14, fontWeight: 500, transition: 'all 0.15s ease' },
  toggleActive: { backgroundColor: '#313244', color: '#cdd6f4', borderColor: '#89b4fa' },
  savedNotice: { marginTop: 16, padding: '8px 12px', borderRadius: 6, backgroundColor: '#1e3a2f', color: '#a6e3a1', fontSize: 13 },
  description: { fontSize: 12, color: '#6c7086', marginTop: 4 },
};

export function SettingsPanel({ onSettingsChange }: any) {
  const { settings, updateSettings } = useAppStore();
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    onSettingsChange?.(settings);
    setSaved(true);
    const timer = setTimeout(() => setSaved(false), 2000);
    return () => clearTimeout(timer);
  }, [settings, onSettingsChange]);

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Settings</h2>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>API URL</label>
        <input style={styles.input} type="text" value={settings.apiUrl} onChange={(e) => updateSettings({ apiUrl: e.target.value })} placeholder="http://localhost:8000" />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Backend API Key</label>
        <input style={styles.input} type="password" value={settings.apiKey || ''} onChange={(e) => updateSettings({ apiKey: e.target.value })} placeholder="Enter API key (optional)" />
        <div style={styles.description}>Required if your backend has authentication enabled</div>
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Theme</label>
        <div style={styles.toggleRow}>
          <button style={{ ...styles.toggleButton, ...(settings.theme === 'dark' ? styles.toggleActive : {}) }} onClick={() => updateSettings({ theme: 'dark' })}>Dark</button>
          <button style={{ ...styles.toggleButton, ...(settings.theme === 'light' ? styles.toggleActive : {}) }} onClick={() => updateSettings({ theme: 'light' })}>Light</button>
        </div>
      </div>

      {saved && <div style={styles.savedNotice}>Settings saved</div>}
    </div>
  );
}
