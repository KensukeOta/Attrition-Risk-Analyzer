<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";
	import { toast } from "svelte-sonner";
	import Spinner from "$lib/components/Spinner/Spinner.svelte";

	let file = $state<File | null>(null);
	let loading = $state(false);
	let errorMessage = $state("");
	let successMessage = $state("");
	let isDragging = $state(false);

	function setFile(f: File | null) {
		if (!f) return;

		if (!f.name.endsWith(".csv")) {
			errorMessage = "CSVファイルを選択してください";
			return;
		}

		file = f;
		errorMessage = "";
		successMessage = "";
	}

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		isDragging = true;
	}

	function handleDragLeave(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragging = false;

		const dropped = e.dataTransfer?.files?.[0] ?? null;

		setFile(dropped);
	}

	async function uploadCsv() {
		if (!file) {
			toast.error("CSVファイルを選択してください");
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

			// 成功toast
			toast.success("CSVをダウンロードしました");
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
			class={`block cursor-pointer rounded-3xl border-2 border-dashed p-8 text-center transition
			${isDragging ? "border-blue-500 bg-blue-50" : "border-slate-300 hover:border-blue-400"}`}
			ondragenter={handleDragOver}
			ondragover={handleDragOver}
			ondragleave={handleDragLeave}
			ondrop={handleDrop}
		>
			<input
				type="file"
				accept=".csv"
				class="hidden"
				onchange={(e) => {
					setFile((e.currentTarget as HTMLInputElement).files?.[0] ?? null);
				}}
			/>

			<div class="space-y-2">
				<p class="text-lg font-semibold text-slate-700">CSVファイルをドラッグ＆ドロップ</p>

				<p class="text-sm text-slate-500">またはクリックして選択</p>

				{#if file}
					<div
						class="mt-4 inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-700"
					>
						{file.name}
					</div>
				{/if}
			</div>
		</label>

		<button
			onclick={uploadCsv}
			disabled={loading}
			class="mt-6 w-full rounded-2xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-400"
		>
			<div class="flex items-center justify-center gap-2">
				{#if loading}
					<Spinner />
					<span>予測中...</span>
				{:else}
					<span>CSV一括予測</span>
				{/if}
			</div>
		</button>
	</div>
</div>
