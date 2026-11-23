<script lang="ts">
  import { enhance } from '$app/forms';
  import { resolve } from '$app/paths';
  import { fade } from 'svelte/transition';
  import '../../../app.css';
  import '#lib/v2/styles/v2.css';
  import { ArrowLeft, ArrowRight, Check, Sparkles, HeartHandshake, TrendingUp, Headphones, Receipt, Target, Users, ShieldCheck, CircleCheck } from '@lucide/svelte';
  import imgLogo from '#lib/assets/images/logo.png';
  import type { PageProps } from './$types';

  let { data, form }: PageProps = $props();
  type Answers = { role: string; industry: string; company_size: string; goals: string[]; current_tool: string; challenge: string };
  let answers = $state<Answers>({ role: data.answers?.role ?? '', industry: data.answers?.industry ?? '', company_size: data.answers?.company_size ?? '', goals: data.answers?.goals ?? [], current_tool: data.answers?.current_tool ?? '', challenge: data.answers?.challenge ?? '' });
  let step = $state(0);
  let saving = $state(false);
  let finishRequested = $state(false);
  const steps = [
    { title: 'What best describes your role?', subtitle: 'We’ll tailor the workspace around the way you work.' },
    { title: 'What kind of business are you in?', subtitle: 'This helps us recommend the right starting point.' },
    { title: 'How big is your team?', subtitle: 'We’ll keep your setup right-sized.' },
    { title: 'What would you like Godan to help with?', subtitle: 'Choose everything that matters to your business.' },
    { title: 'Are you moving from another tool?', subtitle: 'We can help make the transition easier.' },
    { title: 'What’s your biggest workflow challenge?', subtitle: 'Optional — tell us where you want to make progress first.' }
  ];
  const roles = ['Founder / business owner', 'Sales', 'Marketing', 'Customer support', 'Operations', 'Team manager', 'Consultant / agency', 'Other'];
  const industries = ['Technology / SaaS', 'Professional services', 'Retail / e-commerce', 'Manufacturing', 'Financial services', 'Healthcare', 'Education', 'Real estate', 'Hospitality', 'Non-profit', 'Other'];
  const sizes = ['Just me', '2–5 people', '6–10 people', '11–25 people', '26–50 people', '51–100 people', '100+ people'];
  const goals = [
    { label: 'Manage leads', desc: 'Capture and follow up', icon: Target },
    { label: 'Grow sales', desc: 'Pipeline and deals', icon: TrendingUp },
    { label: 'Customer relationships', desc: 'Accounts and contacts', icon: HeartHandshake },
    { label: 'Customer support', desc: 'Tickets and service', icon: Headphones },
    { label: 'Invoices & payments', desc: 'Billing and collections', icon: Receipt },
    { label: 'Team productivity', desc: 'Tasks and collaboration', icon: Users }
  ];
  const progress = $derived(((step + 1) / steps.length) * 100);
  const canContinue = $derived(step === 0 ? !!answers.role : step === 1 ? !!answers.industry : step === 2 ? !!answers.company_size : step === 3 ? answers.goals.length > 0 : true);
  function toggleGoal(goal: string) { answers.goals = answers.goals.includes(goal) ? answers.goals.filter((g) => g !== goal) : [...answers.goals, goal]; }
  function next() { if (step < steps.length - 1) step += 1; }
  function back() { if (step > 0) step -= 1; }
  function submitStep() { finishRequested = step === steps.length - 1; }

  $effect(() => {
    if (step > 0) {
      const currentStep = step;
      requestAnimationFrame(() => {
        if (currentStep === step) document.querySelector('.onboard-step')?.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
      });
    }
  });
</script>

<svelte:head>
  <title>Welcome to Godan · Setup your workspace</title>
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="onboard-root">
  <div class="onboard-top">
    <a class="onboard-brand" href={resolve('')}><img src={imgLogo} alt="" /><span>Godan</span></a>
    <div class="onboard-header-actions"><span class="onboard-secure"><ShieldCheck size={15}/> Personalize your workspace</span><a class="onboard-skip" href={resolve("org/new")}>Skip setup</a></div>
  </div>
  <div class="onboard-progress"><span style:width={progress + '%'}></span></div>
  <main class="onboard-main">
    <div class="onboard-intro">
      <div class="onboard-welcome-icon"><Sparkles size={21}/></div>
      <p class="eyebrow">YOUR WORKSPACE, YOUR WAY</p>
      <h1>Let’s make Godan work<br class="desktop-break"/> for your business.</h1>
      <p class="intro-copy">A few quick questions help us set up a CRM that fits how you work. It takes about a minute.</p>
      <div class="onboard-stepmeta"><span>Step {step + 1} of {steps.length}</span><span>{Math.round(progress)}% complete</span></div>
    </div>
    <form method="POST" action="?/save" use:enhance={() => { saving = true; return async ({ result, update }) => { if (result.type === 'success' && result.data?.saved && !finishRequested) { await update({ reset: false }); next(); } else { await update({ reset: false }); } saving = false; finishRequested = false; }; }}>
      <input type="hidden" name="answers" value={JSON.stringify(answers)} />
      <input type="hidden" name="completed" value={finishRequested ? 'true' : 'false'} />
      {#if data.unavailable}<div class="onboard-error" role="status">We couldn’t load saved onboarding progress right now. You can continue, and we’ll try saving your answers again.</div>{/if}
      {#if form?.error}<div class="onboard-error" role="alert">{form.error}</div>{/if}
      {#key step}
        <div class="onboard-step" in:fade={{ duration: 180 }} out:fade={{ duration: 120 }} aria-live="polite">
          <h2>{steps[step].title}</h2><p class="step-sub">{steps[step].subtitle}</p>
          {#if step === 0}
            <div class="option-grid">
              {#each roles as role (role)}<button type="button" class="option-card" class:selected={answers.role === role} aria-pressed={answers.role === role} onclick={() => answers.role = role}><span>{role}</span>{#if answers.role === role}<Check size={17}/>{/if}</button>{/each}
            </div>
          {:else if step === 1}
            <div class="option-grid">
              {#each industries as industry (industry)}<button type="button" class="option-card" class:selected={answers.industry === industry} aria-pressed={answers.industry === industry} onclick={() => answers.industry = industry}><span>{industry}</span>{#if answers.industry === industry}<Check size={17}/>{/if}</button>{/each}
            </div>
          {:else if step === 2}
            <div class="option-grid">
              {#each sizes as size (size)}<button type="button" class="option-card" class:selected={answers.company_size === size} aria-pressed={answers.company_size === size} onclick={() => answers.company_size = size}><span>{size}</span>{#if answers.company_size === size}<Check size={17}/>{/if}</button>{/each}
            </div>
          {:else if step === 3}
            <div class="goal-grid">
              {#each goals as goal (goal.label)}
                {@const GoalIcon = goal.icon}
                <button type="button" class="goal-card" class:selected={answers.goals.includes(goal.label)} aria-pressed={answers.goals.includes(goal.label)} onclick={() => toggleGoal(goal.label)}><GoalIcon size={20}/><span class="goal-title">{goal.label}</span><small>{goal.desc}</small>{#if answers.goals.includes(goal.label)}<span class="goal-check"><Check size={14}/></span>{/if}</button>
              {/each}
            </div>
          {:else if step === 4}
            <label class="onboard-label" for="current_tool">Current CRM or tools (optional)</label><input class="onboard-input" id="current_tool" bind:value={answers.current_tool} placeholder="e.g. spreadsheets, HubSpot, Salesforce, none" maxlength="120"/><div class="helper">If you’re starting fresh, simply leave this blank.</div>
          {:else}
            <label class="onboard-label" for="challenge">Your biggest challenge (optional)</label><textarea class="onboard-input onboard-textarea" id="challenge" bind:value={answers.challenge} placeholder="e.g. We lose track of follow-ups and customer conversations…" maxlength="500"></textarea><div class="helper">This helps us understand what success looks like for you.</div>
          {/if}
        </div>
      {/key}
      <div class="onboard-actions">
        <button class="onboard-back" type="button" onclick={back} disabled={step === 0 || saving}><ArrowLeft size={16}/> Back</button>
        <button class="onboard-next" type="submit" disabled={!canContinue || saving} onclick={submitStep}>{#if saving}<span class="onboard-spinner"></span> Saving…{:else if step === steps.length - 1}<span>Continue to organization</span><ArrowRight size={17}/>{:else}<span>Continue</span><ArrowRight size={17}/>{/if}</button>
      </div>
    </form>
    <p class="onboard-foot"><CircleCheck size={14}/> Your answers are saved securely and can be updated later.</p>
  </main>
</div>

<style>
  .onboard-root{min-height:100dvh;background:radial-gradient(ellipse at 18% 0%,#fff1e7 0,transparent 38%),radial-gradient(ellipse at 100% 80%,#f3f5fb 0,transparent 42%),#fbfaf9;color:#20232b;font-family:system-ui,-apple-system,'Segoe UI',sans-serif}
  .onboard-top{height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 clamp(20px,5vw,72px);border-bottom:1px solid #e9e7e4;background:rgba(255,255,255,.65);backdrop-filter:blur(14px)}
  .onboard-brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#20232b;font-size:20px;font-weight:800;letter-spacing:-.04em}.onboard-brand img{width:30px;height:30px;object-fit:contain}
  .onboard-header-actions{display:flex;align-items:center;gap:20px}.onboard-secure{display:flex;align-items:center;gap:7px;font-size:12px;color:#6f737c}.onboard-skip{font-size:12px;color:#777c85;text-decoration:none}.onboard-skip:hover{color:#ea580c;text-decoration:underline}
  .onboard-progress{height:3px;background:#eee8e2}.onboard-progress span{display:block;height:100%;background:linear-gradient(90deg,#f97316,#ea580c);transition:width .45s cubic-bezier(.2,.8,.2,1)}
  .onboard-main{max-width:780px;margin:0 auto;padding:clamp(28px,5vw,56px) 22px 28px}
  .onboard-intro{text-align:center;margin-bottom:36px}.onboard-welcome-icon{display:grid;place-items:center;width:48px;height:48px;margin:0 auto 14px;border-radius:16px;background:#fff1e7;color:#ea580c;box-shadow:0 4px 20px #f9731618}.eyebrow{font-size:11px;font-weight:700;letter-spacing:.16em;color:#ea580c;margin:0 0 10px}
  h1{font-weight:800;font-size:clamp(29px,4.3vw,43px);line-height:1.14;letter-spacing:-.045em;margin:0;color:#20232b}.intro-copy{max-width:520px;margin:15px auto 22px;color:#747984;line-height:1.65;font-size:14px}.onboard-stepmeta{display:flex;justify-content:space-between;max-width:500px;margin:0 auto;color:#8a8d95;font-size:12px}
  form{background:#fff;border:1px solid #ebe8e5;border-radius:24px;padding:clamp(20px,4vw,34px);box-shadow:0 12px 44px rgba(31,35,41,.045)}h2{font-weight:700;font-size:22px;line-height:1.3;letter-spacing:-.025em;margin:0}.step-sub{color:#777c85;font-size:13px;margin:7px 0 24px}
  .option-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.option-card{display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:54px;border:1px solid #e9e8e6;background:#fff;border-radius:13px;padding:12px 15px;text-align:left;font-size:13px;color:#454952;cursor:pointer;transition:transform .18s,border-color .18s,background .18s,box-shadow .18s}.option-card:hover{transform:translateY(-1px);border-color:#f4b38c;box-shadow:0 6px 18px #ea580c0a}.option-card.selected{border-color:#ea580c;background:#fff7f1;color:#b64a0b;box-shadow:inset 0 0 0 1px #ea580c}
  .goal-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}.goal-card{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:7px;min-height:126px;padding:17px;border:1px solid #e9e8e6;border-radius:14px;background:#fff;color:#646a74;text-align:left;cursor:pointer;transition:transform .18s,border .18s,background .18s}.goal-card:hover{transform:translateY(-2px);border-color:#f4b38c}.goal-card.selected{background:#fff7f1;border-color:#ea580c;color:#c14e0b;box-shadow:inset 0 0 0 1px #ea580c}.goal-title{font-size:13px;font-weight:700;color:#333740}.goal-card small{font-size:11px;color:#898d95}.goal-check{position:absolute;right:10px;top:10px;display:grid;place-items:center;background:#ea580c;color:#fff;width:19px;height:19px;border-radius:50%}
  .onboard-label{display:block;font-size:13px;font-weight:600;margin-bottom:8px}.onboard-input{width:100%;padding:14px 15px;border:1px solid #dededb;border-radius:12px;font:inherit;font-size:14px;color:#20232b;background:#fff;outline:none;transition:border .2s,box-shadow .2s}.onboard-input:focus{border-color:#ea580c;box-shadow:0 0 0 3px #ea580c18}.onboard-textarea{min-height:120px;resize:vertical}.helper{font-size:12px;color:#8b8f97;margin-top:8px}
  .onboard-actions{display:flex;align-items:center;justify-content:space-between;margin-top:28px}.onboard-back{border:0;background:none;color:#6d727b;display:flex;align-items:center;gap:8px;padding:10px 6px;font-size:13px;cursor:pointer}.onboard-back:disabled{opacity:.35;cursor:default}.onboard-next{display:flex;align-items:center;justify-content:center;gap:10px;min-width:150px;padding:13px 19px;border:0;border-radius:12px;background:#ea580c;color:white;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 6px 18px #ea580c20;transition:transform .18s,background .18s}.onboard-next:hover:not(:disabled){transform:translateY(-1px);background:#d94f08}.onboard-next:disabled{opacity:.55;cursor:not-allowed}.onboard-spinner{width:14px;height:14px;border:2px solid #ffffff70;border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite}.onboard-foot{display:flex;align-items:center;justify-content:center;gap:7px;margin:19px 0 0;color:#9a9da4;font-size:11px}.onboard-foot svg{color:#67a57d}.onboard-error{background:#fff0ed;color:#b42318;padding:10px 12px;border-radius:10px;margin-bottom:16px}
  @keyframes spin{to{transform:rotate(360deg)}}
  @media(max-width:640px){.onboard-top{height:58px;padding:0 18px}.onboard-header-actions{gap:12px}.onboard-secure{font-size:10px}.onboard-main{padding-top:28px}.onboard-intro{margin-bottom:25px}.option-grid{grid-template-columns:1fr}.goal-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.goal-card{min-height:116px;padding:14px}.desktop-break{display:none}form{border-radius:18px}.onboard-next{min-width:138px}}
  @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>
