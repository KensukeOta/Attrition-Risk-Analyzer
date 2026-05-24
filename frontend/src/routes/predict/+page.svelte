<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";
	import Spinner from "$lib/components/Spinner/Spinner.svelte";

	type PredictionResult = {
		attrition_probability: number;
		prediction: string;
		risk_level: "High" | "Middle" | "Low";
		threshold: number;
		risk_factors: string[];
	};

	type FieldConfig = {
		key: keyof typeof form;
		label: string;
		type: "number" | "select";
		options?: string[];
		min?: number;
		max?: number;
	};

	type SectionConfig = {
		title: string;
		description: string;
		fields: FieldConfig[];
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

	const sections: SectionConfig[] = [
		{
			title: "基本情報",
			description: "年齢・性別・婚姻状況・学歴などの基本属性です。",
			fields: [
				{
					key: "Age",
					label: "年齢",
					type: "number",
					min: 18,
					max: 65
				},
				{
					key: "Gender",
					label: "性別",
					type: "select",
					options: ["Male", "Female"]
				},
				{
					key: "MaritalStatus",
					label: "婚姻状況",
					type: "select",
					options: ["Single", "Married", "Divorced"]
				},
				{
					key: "Education",
					label: "学歴レベル",
					type: "number",
					min: 1,
					max: 5
				},
				{
					key: "EducationField",
					label: "専攻分野",
					type: "select",
					options: [
						"Life Sciences",
						"Medical",
						"Marketing",
						"Technical Degree",
						"Human Resources",
						"Other"
					]
				}
			]
		},
		{
			title: "勤務条件",
			description: "部署・職種・出張・残業・通勤距離などの勤務条件です。",
			fields: [
				{
					key: "Department",
					label: "部署",
					type: "select",
					options: ["Sales", "Research & Development", "Human Resources"]
				},
				{
					key: "JobRole",
					label: "職種",
					type: "select",
					options: [
						"Sales Executive",
						"Research Scientist",
						"Laboratory Technician",
						"Manufacturing Director",
						"Healthcare Representative",
						"Manager",
						"Sales Representative",
						"Research Director",
						"Human Resources"
					]
				},
				{
					key: "BusinessTravel",
					label: "出張頻度",
					type: "select",
					options: ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
				},
				{
					key: "OverTime",
					label: "残業",
					type: "select",
					options: ["Yes", "No"]
				},
				{
					key: "DistanceFromHome",
					label: "通勤距離",
					type: "number",
					min: 1
				},
				{
					key: "JobInvolvement",
					label: "仕事への関与度",
					type: "number",
					min: 1,
					max: 4
				},
				{
					key: "JobLevel",
					label: "職位レベル",
					type: "number",
					min: 1,
					max: 5
				}
			]
		},
		{
			title: "給与・待遇",
			description: "給与・レート・昇給率・ストックオプションなどの待遇情報です。",
			fields: [
				{
					key: "MonthlyIncome",
					label: "月収",
					type: "number",
					min: 0
				},
				{
					key: "DailyRate",
					label: "日給レート",
					type: "number",
					min: 0
				},
				{
					key: "HourlyRate",
					label: "時給レート",
					type: "number",
					min: 0
				},
				{
					key: "MonthlyRate",
					label: "月額レート",
					type: "number",
					min: 0
				},
				{
					key: "PercentSalaryHike",
					label: "昇給率",
					type: "number",
					min: 0
				},
				{
					key: "StockOptionLevel",
					label: "ストックオプションレベル",
					type: "number",
					min: 0,
					max: 3
				}
			]
		},
		{
			title: "満足度",
			description: "仕事・職場環境・人間関係・ワークライフバランスの評価です。",
			fields: [
				{
					key: "JobSatisfaction",
					label: "仕事満足度",
					type: "number",
					min: 1,
					max: 4
				},
				{
					key: "EnvironmentSatisfaction",
					label: "職場環境満足度",
					type: "number",
					min: 1,
					max: 4
				},
				{
					key: "RelationshipSatisfaction",
					label: "人間関係満足度",
					type: "number",
					min: 1,
					max: 4
				},
				{
					key: "WorkLifeBalance",
					label: "ワークライフバランス",
					type: "number",
					min: 1,
					max: 4
				}
			]
		},
		{
			title: "キャリア",
			description: "経験年数・勤続年数・昇進・上司との年数などのキャリア情報です。",
			fields: [
				{
					key: "TotalWorkingYears",
					label: "総経験年数",
					type: "number",
					min: 0
				},
				{
					key: "YearsAtCompany",
					label: "勤続年数",
					type: "number",
					min: 0
				},
				{
					key: "YearsInCurrentRole",
					label: "現在の役割での年数",
					type: "number",
					min: 0
				},
				{
					key: "YearsSinceLastPromotion",
					label: "前回昇進からの年数",
					type: "number",
					min: 0
				},
				{
					key: "YearsWithCurrManager",
					label: "現在の上司との年数",
					type: "number",
					min: 0
				},
				{
					key: "NumCompaniesWorked",
					label: "過去に働いた会社数",
					type: "number",
					min: 0
				},
				{
					key: "TrainingTimesLastYear",
					label: "昨年の研修回数",
					type: "number",
					min: 0
				}
			]
		}
	];

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
			class="space-y-6"
			onsubmit={(e) => {
				e.preventDefault();
				predict();
			}}
		>
			{#each sections as section}
				<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
					<div class="mb-5">
						<h2 class="text-xl font-bold text-slate-900">
							{section.title}
						</h2>
						<p class="mt-1 text-sm text-slate-500">
							{section.description}
						</p>
					</div>

					<div class="grid gap-4 sm:grid-cols-2">
						{#each section.fields as field}
							<label class="space-y-1">
								<span class="text-sm font-medium text-slate-700">
									{field.label}
									<span class="ml-1 text-xs text-slate-400">
										({field.key})
									</span>
								</span>

								{#if field.type === "select"}
									<select
										bind:value={form[field.key]}
										class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 transition outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
									>
										{#each field.options ?? [] as option}
											<option value={option}>
												{option}
											</option>
										{/each}
									</select>
								{:else}
									<input
										type="number"
										min={field.min}
										max={field.max}
										bind:value={form[field.key]}
										class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 transition outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
									/>
								{/if}
							</label>
						{/each}
					</div>
				</section>
			{/each}

			<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
				<button
					type="submit"
					disabled={loading}
					class="w-full rounded-2xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-400"
				>
					<div class="flex items-center justify-center gap-2">
						{#if loading}
							<Spinner />
							<span>予測中...</span>
						{:else}
							<span>予測する</span>
						{/if}
					</div>
				</button>

				{#if errorMessage}
					<p class="mt-3 font-medium text-red-600">
						{errorMessage}
					</p>
				{/if}
			</div>
		</form>

		<aside
			class="sticky top-6 self-start rounded-3xl border border-slate-200 bg-white p-6 shadow-lg"
		>
			<h2 class="mb-4 text-xl font-bold text-slate-900">予測結果</h2>

			{#if result}
				<div class={`inline-flex rounded-full px-4 py-2 text-sm font-bold ${riskColor}`}>
					{result.risk_level}
				</div>

				<p class="mt-5 text-5xl font-black text-slate-900">
					{(result.attrition_probability * 100).toFixed(1)}%
				</p>

				<p class="mt-2 text-sm text-slate-500">
					離職予測:
					<span class="font-semibold text-slate-900">
						{result.prediction}
					</span>
				</p>

				<p class="text-sm text-slate-500">
					判定閾値:
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
		</aside>
	</div>
</div>
