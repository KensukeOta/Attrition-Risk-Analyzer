<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";

	type PredictionResult = {
		attrition_probability: number;
		prediction: string;
		risk_level: "High" | "Middle" | "Low";
		threshold: number;
		risk_factors: string[];
	};

	let form = $state({
		Age: 35,
		BusinessTravel: "Travel_Rarely",
		DailyRate: 1100,
		Department: "Sales",
		DistanceFromHome: 12,
		Education: 3,
		EducationField: "Life Sciences",
		EnvironmentSatisfaction: 2,
		Gender: "Male",
		HourlyRate: 80,
		JobInvolvement: 3,
		JobLevel: 2,
		JobRole: "Sales Executive",
		JobSatisfaction: 2,
		MaritalStatus: "Single",
		MonthlyIncome: 5000,
		MonthlyRate: 15000,
		NumCompaniesWorked: 2,
		OverTime: "Yes",
		PercentSalaryHike: 12,
		RelationshipSatisfaction: 3,
		StockOptionLevel: 0,
		TotalWorkingYears: 8,
		TrainingTimesLastYear: 2,
		WorkLifeBalance: 2,
		YearsAtCompany: 5,
		YearsInCurrentRole: 3,
		YearsSinceLastPromotion: 1,
		YearsWithCurrManager: 3
	});

	let result = $state<PredictionResult | null>(null);
	let loading = $state(false);
	let errorMessage = $state("");

	const riskColor = $derived(
		result?.risk_level === "High"
			? "bg-red-100 text-red-700"
			: result?.risk_level === "Middle"
				? "bg-yellow-100 text-yellow-700"
				: "bg-green-100 text-green-700"
	);

	async function predict() {
		loading = true;
		errorMessage = "";
		result = null;

		try {
			const res = await fetch(`${PUBLIC_API_URL}/api/v1/predict`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify(form)
			});

			if (!res.ok) {
				throw new Error("予測に失敗しました");
			}

			result = await res.json();
		} catch (e) {
			errorMessage = e instanceof Error ? e.message : "予期しないエラーが発生しました";
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>離職リスク予測</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-10">
	<div class="mb-8">
		<p class="text-sm font-semibold tracking-widest text-slate-500 uppercase">
			Attrition Risk Analyzer
		</p>

		<h1 class="mt-2 text-4xl font-black text-slate-900">社員の離職リスクを予測</h1>

		<p class="mt-3 max-w-2xl text-slate-600">
			社員データを入力すると、学習済みLightGBMモデルが
			離職確率・リスクレベル・主要なリスク要因を表示します。
		</p>
	</div>

	<div class="grid gap-6 lg:grid-cols-[2fr_1fr]">
		<form
			class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg"
			onsubmit={(e) => {
				e.preventDefault();
				predict();
			}}
		>
			<h2 class="mb-5 text-xl font-bold text-slate-900">社員データ入力</h2>

			<div class="grid gap-4 sm:grid-cols-2">
				<label class="space-y-1">
					<span class="text-sm font-medium">Age</span>
					<input
						type="number"
						bind:value={form.Age}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					/>
				</label>

				<label class="space-y-1">
					<span class="text-sm font-medium">OverTime</span>
					<select
						bind:value={form.OverTime}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					>
						<option value="Yes">Yes</option>
						<option value="No">No</option>
					</select>
				</label>

				<label class="space-y-1">
					<span class="text-sm font-medium">MonthlyIncome</span>
					<input
						type="number"
						bind:value={form.MonthlyIncome}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					/>
				</label>

				<label class="space-y-1">
					<span class="text-sm font-medium">JobSatisfaction</span>
					<input
						type="number"
						min="1"
						max="4"
						bind:value={form.JobSatisfaction}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					/>
				</label>

				<label class="space-y-1">
					<span class="text-sm font-medium"> EnvironmentSatisfaction </span>

					<input
						type="number"
						min="1"
						max="4"
						bind:value={form.EnvironmentSatisfaction}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					/>
				</label>

				<label class="space-y-1">
					<span class="text-sm font-medium"> DistanceFromHome </span>

					<input
						type="number"
						bind:value={form.DistanceFromHome}
						class="w-full rounded-xl border border-slate-300 px-3 py-2"
					/>
				</label>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="mt-6 w-full rounded-2xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-400"
			>
				{loading ? "予測中..." : "予測する"}
			</button>

			{#if errorMessage}
				<p class="mt-3 font-medium text-red-600">
					{errorMessage}
				</p>
			{/if}
		</form>

		<div class="sticky top-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
			<h2 class="mb-4 text-xl font-bold text-slate-900">予測結果</h2>

			{#if result}
				<div class={`inline-flex rounded-full px-4 py-2 text-sm font-bold ${riskColor}`}>
					{result.risk_level}
				</div>

				<p class="mt-5 text-5xl font-black text-slate-900">
					{(result.attrition_probability * 100).toFixed(1)}%
				</p>

				<p class="mt-2 text-sm text-slate-500">
					Prediction:
					<span class="font-semibold text-slate-900">
						{result.prediction}
					</span>
				</p>

				<p class="text-sm text-slate-500">
					Threshold:
					<span class="font-semibold text-slate-900">
						{result.threshold}
					</span>
				</p>

				<h3 class="mt-6 font-semibold text-slate-900">主要なリスク要因</h3>

				<ul class="mt-3 space-y-2 text-sm text-slate-600">
					{#each result.risk_factors as factor}
						<li class="rounded-xl bg-slate-50 px-3 py-2">
							{factor}
						</li>
					{/each}
				</ul>
			{:else}
				<p class="text-slate-500">予測結果はここに表示されます。</p>
			{/if}
		</div>
	</div>
</div>
