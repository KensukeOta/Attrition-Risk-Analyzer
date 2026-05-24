<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";

	type ModelMetrics = {
		model_name: string;
		validation_method: string;
		threshold_strategy: string;
		threshold: number;
		test_metrics: {
			roc_auc: number;
			accuracy: number;
			precision_yes: number;
			recall_yes: number;
			f1_yes: number;
		};
		confusion_matrix: {
			tn: number;
			fp: number;
			fn: number;
			tp: number;
		};
		class_distribution: {
			no: number;
			yes: number;
		};
	};

	let metrics = $state<ModelMetrics | null>(null);
	let loading = $state(true);
	let errorMessage = $state("");

	async function fetchMetrics() {
		loading = true;
		errorMessage = "";

		try {
			const res = await fetch(`${PUBLIC_API_URL}/api/v1/model/metrics`);

			if (!res.ok) {
				throw new Error("モデル評価指標の取得に失敗しました");
			}

			metrics = await res.json();
		} catch (e) {
			errorMessage = e instanceof Error ? e.message : "予期しないエラーが発生しました";
		} finally {
			loading = false;
		}
	}

	function percent(value: number) {
		return `${(value * 100).toFixed(1)}%`;
	}

	fetchMetrics();
</script>

<svelte:head>
	<title>モデル評価</title>
</svelte:head>

<div class="mx-auto max-w-6xl px-4 py-10">
	<div class="mb-8">
		<p class="text-sm font-semibold tracking-widest text-slate-500 uppercase">Model Evaluation</p>

		<h1 class="mt-2 text-4xl font-black text-slate-900">モデル評価</h1>

		<p class="mt-3 max-w-3xl text-slate-600">
			テストデータに対するLightGBMモデルの評価結果です。
			離職予測では、離職者の見逃しを減らすためにRecallを重視しています。
		</p>
	</div>

	{#if loading}
		<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
			<p class="text-slate-500">読み込み中...</p>
		</div>
	{:else if errorMessage}
		<div class="rounded-3xl border border-red-200 bg-red-50 p-6">
			<p class="font-medium text-red-700">{errorMessage}</p>
		</div>
	{:else if metrics}
		<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
			<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-semibold text-slate-500">ROC-AUC</p>
				<p class="mt-3 text-3xl leading-none font-black text-slate-900">
					{metrics.test_metrics.roc_auc.toFixed(3)}
				</p>
			</div>

			<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-semibold text-slate-500">Accuracy</p>
				<p class="mt-3 text-3xl leading-none font-black text-slate-900">
					{percent(metrics.test_metrics.accuracy)}
				</p>
			</div>

			<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-semibold text-slate-500">Precision(Yes)</p>
				<p class="mt-3 text-3xl leading-none font-black text-slate-900">
					{percent(metrics.test_metrics.precision_yes)}
				</p>
			</div>

			<div class="rounded-3xl border border-blue-200 bg-blue-50 p-6 shadow-sm">
				<p class="text-sm font-semibold text-blue-600">Recall(Yes)</p>
				<p class="mt-3 text-3xl leading-none font-black text-blue-900">
					{percent(metrics.test_metrics.recall_yes)}
				</p>
			</div>

			<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-semibold text-slate-500">F1(Yes)</p>
				<p class="mt-3 text-3xl leading-none font-black text-slate-900">
					{percent(metrics.test_metrics.f1_yes)}
				</p>
			</div>
		</div>

		<div class="mt-6 grid gap-6 lg:grid-cols-[1.2fr_1fr]">
			<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
				<h2 class="text-xl font-bold text-slate-900">Confusion Matrix</h2>

				<p class="mt-1 text-sm text-slate-500">行が実際のクラス、列が予測クラスです。</p>

				<div class="mt-6 overflow-hidden rounded-2xl border border-slate-200">
					<table class="w-full border-collapse text-center">
						<thead class="bg-slate-50">
							<tr>
								<th class="border-b border-slate-200 p-4"></th>
								<th class="border-b border-slate-200 p-4 font-bold text-slate-700"> 予測 No </th>
								<th class="border-b border-slate-200 p-4 font-bold text-slate-700"> 予測 Yes </th>
							</tr>
						</thead>

						<tbody>
							<tr>
								<th
									class="border-r border-b border-slate-200 bg-slate-50 p-4 text-left font-bold text-slate-700"
								>
									実際 No
								</th>

								<td class="border-r border-b border-slate-200 p-6">
									<p class="text-3xl font-black text-green-700">
										{metrics.confusion_matrix.tn}
									</p>
									<p class="mt-1 text-xs text-slate-500">TN</p>
								</td>

								<td class="border-b border-slate-200 p-6">
									<p class="text-3xl font-black text-yellow-700">
										{metrics.confusion_matrix.fp}
									</p>
									<p class="mt-1 text-xs text-slate-500">FP</p>
								</td>
							</tr>

							<tr>
								<th
									class="border-r border-slate-200 bg-slate-50 p-4 text-left font-bold text-slate-700"
								>
									実際 Yes
								</th>

								<td class="border-r border-slate-200 p-6">
									<p class="text-3xl font-black text-red-700">
										{metrics.confusion_matrix.fn}
									</p>
									<p class="mt-1 text-xs text-slate-500">FN</p>
								</td>

								<td class="p-6">
									<p class="text-3xl font-black text-green-700">
										{metrics.confusion_matrix.tp}
									</p>
									<p class="mt-1 text-xs text-slate-500">TP</p>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</section>

			<aside class="space-y-6">
				<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
					<h2 class="text-lg font-bold text-slate-900">評価設定</h2>

					<div class="mt-4 space-y-3 text-sm text-slate-600">
						<p>
							<span class="font-semibold text-slate-900">モデル:</span>
							{metrics.model_name}
						</p>

						<p>
							<span class="font-semibold text-slate-900">検証方法:</span>
							{metrics.validation_method}
						</p>

						<p>
							<span class="font-semibold text-slate-900">判定閾値:</span>
							{metrics.threshold}
						</p>
					</div>
				</section>

				<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
					<h2 class="text-lg font-bold text-slate-900">閾値最適化</h2>

					<p class="mt-4 text-sm leading-7 text-slate-600">
						{metrics.threshold_strategy}
					</p>
				</section>

				<section class="rounded-3xl border border-blue-200 bg-blue-50 p-6 shadow-sm">
					<h2 class="text-lg font-bold text-blue-900">このモデルの方針</h2>

					<p class="mt-4 text-sm leading-7 text-blue-800">
						離職予測では、実際に離職する可能性がある社員を見逃さないことを重視しています。
						そのため、AccuracyだけでなくRecall(Yes)を重視して評価しています。
					</p>
				</section>
			</aside>
		</div>
	{/if}
</div>
