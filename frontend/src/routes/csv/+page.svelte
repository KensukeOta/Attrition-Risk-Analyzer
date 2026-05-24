<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";

	let file = $state<File | null>(null);
	let loading = $state(false);
	let errorMessage = $state("");
	let successMessage = $state("");

	async function uploadCsv() {
		if (!file) {
			errorMessage = "CSVファイルを選択してください";
			return;
		}

		loading = true;
		errorMessage = "";
		successMessage = "";

		try {
			const formData = new FormData();
			formData.append("file", file);

			const res = await fetch(`${PUBLIC_API_URL}/api/v1/predict/csv`, {
				method: "POST",
				body: formData
			});

			if (!res.ok) {
				throw new Error("CSV予測に失敗しました");
			}

			const blob = await res.blob();

			const url = window.URL.createObjectURL(blob);

			const a = document.createElement("a");

			a.href = url;
			a.download = "prediction_result.csv";

			document.body.appendChild(a);
			a.click();
			a.remove();

			window.URL.revokeObjectURL(url);

			successMessage = "予測結果CSVをダウンロードしました";
		} catch (e) {
			errorMessage = e instanceof Error ? e.message : "予期しないエラー";
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>CSV一括予測</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-10">
	<div class="mb-8">
		<p class="text-sm font-semibold tracking-widest text-slate-500 uppercase">
			Attrition Risk Analyzer
		</p>

		<h1 class="mt-2 text-4xl font-black text-slate-900">CSV一括予測</h1>

		<p class="mt-3 text-slate-600">
			社員データCSVをアップロードすると、 離職確率・リスクレベル付きCSVを ダウンロードできます。
		</p>
	</div>

	<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
		<label
			class="block rounded-2xl border-2 border-dashed border-slate-300 p-6 text-center transition hover:border-blue-400"
		>
			<input
				type="file"
				accept=".csv"
				class="hidden"
				onchange={(e) => {
					file = (e.currentTarget as HTMLInputElement).files?.[0] ?? null;
				}}
			/>

			<p class="font-medium text-slate-700">CSVファイルを選択</p>

			<p class="mt-1 text-sm text-slate-500">
				{file ? file.name : "クリックしてCSVを選択"}
			</p>
		</label>

		<button
			onclick={uploadCsv}
			disabled={loading}
			class="mt-6 w-full rounded-2xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-400"
		>
			{loading ? "予測中..." : "CSV一括予測"}
		</button>

		{#if errorMessage}
			<p class="mt-4 font-medium text-red-600">
				{errorMessage}
			</p>
		{/if}

		{#if successMessage}
			<p class="mt-4 font-medium text-green-600">
				{successMessage}
			</p>
		{/if}
	</div>
</div>
