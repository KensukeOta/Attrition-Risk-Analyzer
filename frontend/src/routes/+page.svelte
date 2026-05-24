<script lang="ts">
	const cards = [
		{
			title: "単体予測",
			description: "社員1人分のデータを入力し、離職確率・リスクレベルを表示します。",
			href: "/predict"
		},
		{
			title: "CSV一括予測",
			description: "社員データCSVをアップロードし、予測結果付きCSVをダウンロードします。",
			href: "/csv"
		},
		{
			title: "特徴量重要度",
			description: "LightGBMの特徴量重要度を平均・標準偏差・安定性とともに確認します。",
			href: "/feature-importance"
		},
		{
			title: "モデル評価",
			description: "ROC-AUC、Recall、Confusion Matrixなどの評価結果を確認します。",
			href: "/metrics"
		}
	];
</script>

<svelte:head>
	<title>Attrition Risk Analyzer</title>
</svelte:head>

<main class="mx-auto max-w-7xl px-4 py-16">
	<section class="rounded-3xl bg-white p-8 shadow-lg md:p-12">
		<p class="text-sm font-semibold tracking-widest text-blue-600 uppercase">
			Machine Learning Web App
		</p>

		<h1 class="mt-4 max-w-4xl text-4xl leading-tight font-black text-slate-900 md:text-6xl">
			社員の離職リスクを、機械学習モデルで可視化する
		</h1>

		<p class="mt-6 max-w-3xl text-lg leading-8 text-slate-600">
			LightGBMで学習した離職予測モデルをFastAPIに組み込み、
			SvelteKitのUIから単体予測・CSV一括予測・モデル解釈・評価結果を確認できます。
		</p>

		<div class="mt-8 flex flex-wrap gap-3">
			<a
				href="/predict"
				class="rounded-2xl bg-blue-600 px-5 py-3 font-bold text-white transition hover:bg-blue-700"
			>
				予測を試す
			</a>

			<a
				href="/metrics"
				class="rounded-2xl border border-slate-300 px-5 py-3 font-bold text-slate-700 transition hover:bg-slate-100"
			>
				モデル評価を見る
			</a>
		</div>
	</section>

	<section class="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
		{#each cards as card}
			<a
				href={card.href}
				class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
			>
				<h2 class="text-xl font-bold text-slate-900">
					{card.title}
				</h2>

				<p class="mt-3 text-sm leading-6 text-slate-600">
					{card.description}
				</p>
			</a>
		{/each}
	</section>
</main>
