(() => {
  const root = document.documentElement;
  const systemTheme = matchMedia("(prefers-color-scheme: dark)");
  const key = "fn-theme";
  let preference;

  try {
    preference = localStorage.getItem(key);
  } catch {
    preference = null;
  }

  function setTheme(theme) {
    root.dataset.theme = theme;
    const dark = theme === "dark";
    const color = dark ? "#111214" : "#f2f3f4";
    for (const meta of document.querySelectorAll('meta[name="theme-color"]')) {
      meta.content = color;
    }
    const button = document.querySelector("#theme-button");
    if (button) button.setAttribute("aria-label", dark ? "Use light theme" : "Use dark theme");
  }

  const systemChoice = () => systemTheme.matches ? "dark" : "light";

  root.classList.add("js");
  setTheme(preference === "dark" || preference === "light" ? preference : systemChoice());
  systemTheme.addEventListener("change", () => {
    if (preference !== "dark" && preference !== "light") setTheme(systemChoice());
  });

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#theme-button");
    if (!button) return;
    setTheme(root.dataset.theme);
    button.hidden = false;
    button.addEventListener("click", () => {
      preference = root.dataset.theme === "dark" ? "light" : "dark";
      try {
        localStorage.setItem(key, preference);
      } catch {
        // The current page can still apply the requested appearance.
      }
      setTheme(preference);
    });
  });
})();
