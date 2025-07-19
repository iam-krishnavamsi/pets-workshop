<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  type Theme = {
    name: string;
    label: string;
    preview: string;
    className: string;
  };

  const themes: Theme[] = [
    {
      name: 'default',
      label: 'Default',
      preview: '🌑',
      className: 'theme-default',
    },
    {
      name: 'retro',
      label: "80s Retro",
      preview: '🕹️',
      className: 'theme-retro',
    },
    {
      name: 'terminal',
      label: 'Terminal Classic',
      preview: '💻',
      className: 'theme-terminal',
    },
    {
      name: 'sketch',
      label: 'Hand-Sketched',
      preview: '✏️',
      className: 'theme-sketch',
    },
    {
      name: 'steampunk',
      label: 'Steampunk',
      preview: '⚙️',
      className: 'theme-steampunk',
    },
    {
      name: 'fantasy',
      label: 'Fantasy Realm',
      preview: '🧙',
      className: 'theme-fantasy',
    },
  ];

  const themeStore = writable('default');

  const setTheme = (theme: string) => {
    themeStore.set(theme);
    document.body.className = '';
    document.body.classList.add(themes.find(t => t.name === theme)?.className || 'theme-default');
  };

  onMount(() => {
    themeStore.subscribe(setTheme);
  });
</script>

<style>
.theme-selector {
  position: absolute;
  top: 1rem;
  right: 2rem;
  z-index: 100;
  background: var(--theme-bg, #222);
  color: var(--theme-fg, #fff);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  border: none;
  outline: none;
  transition: background 0.3s;
}
.theme-selector select {
  background: transparent;
  color: inherit;
  border: none;
  font-size: 1rem;
  outline: none;
  cursor: pointer;
}
.theme-selector option {
  color: #222;
}
</style>

<div class="theme-selector" aria-label="Theme Selector">
  <span>🎨</span>
  <select on:change={e => setTheme(e.target.value)} aria-label="Select theme">
    {#each themes as theme}
      <option value={theme.name} selected={theme.name === 'default'}>
        {theme.preview} {theme.label}
      </option>
    {/each}
  </select>
</div>
