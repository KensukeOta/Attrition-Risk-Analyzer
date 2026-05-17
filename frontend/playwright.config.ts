import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
	webServer: { command: "npm run build && npm run preview", port: 4173 },
	testDir: "./e2e",
	use: {
		/* Base URL to use in actions like `await page.goto('/')`. */
		baseURL: "http://localhost:5173",

		/* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
		trace: "on-first-retry"
	},

	/* Configure projects for major browsers */
	projects: [
		{
			name: "chromium",
			use: { ...devices["Desktop Chrome"] }
		},

		{
			name: "firefox",
			use: { ...devices["Desktop Firefox"] }
		},

		// {
		//   name: "webkit",
		//   use: { ...devices["Desktop Safari"] },
		// },

		/* Test against mobile viewports. */
		{
			name: "Mobile Chrome",
			use: { ...devices["Pixel 5"] }
		}
	]
});
