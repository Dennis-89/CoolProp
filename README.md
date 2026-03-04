# CustomGas
Just [Download the docs](https://github.com/Dennis-89/CoolProp/blob/main/CustomGas/docs/build/html/index.html) or read below and have fun!

<h1>CustomGas documentation</h1>
<p>A thinny wrapper for the <cite>CoolProp</cite> low-level interface.</p>
<dl class="py class">
<dt class="sig sig-object py" id="customgas.Gas">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">customgas.</span></span><span class="sig-name descname"><span class="pre">Gas</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">backend</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.Gas" title="Link to this definition"></a></dt>
<dd><p>Wrapper for the <a class="reference external" href="https://coolprop.org/">CoolProp</a>-Lowlevel-API to get a more readable
and cleaner source code. The free backend ‘HEOS’ is used.
Use <cite>new()</cite> function to create a <cite>Gas</cite> instance.</p>
<dl class="py method">
<dt class="sig sig-object py" id="customgas.Gas.__init__">
<span class="sig-name descname"><span class="pre">__init__</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">backend</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.Gas.__init__" title="Link to this definition"></a></dt>
<dd><p>See <a class="reference internal" href="#customgas.Gas.new" title="customgas.Gas.new"><code class="xref py py-func docutils literal notranslate"><span class="pre">Gas.new()</span></code></a> for creating a <cite>Gas</cite> instance.</p>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="customgas.Gas.input_pair">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">input_pair</span></span><a class="headerlink" href="#customgas.Gas.input_pair" title="Link to this definition"></a></dt>
<dd><p>Get or set the input-pair. You have to use one of the InputPairs-constant
or import something like that from the <cite>CoolProp</cite>.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>value</strong> – InputPairs-like object. See <a class="reference internal" href="#customgas.InputPairs" title="customgas.InputPairs"><code class="xref py py-func docutils literal notranslate"><span class="pre">InputPairs()</span></code></a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="customgas.Gas.new">
<span class="property"><span class="k"><span class="pre">classmethod</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">new</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.Gas.new" title="Link to this definition"></a></dt>
<dd><p>Function to create a new <cite>Gas</cite> instance. The <cite>name</cite> argument specifies the gas name. To create a gas mixture,
use the <cite>gas_mix</cite> and <cite>percent</cite> keyword arguments. Example: <cite>percent</cite> is a constant of the <cite>Percent</cite>-object
and indicates whether it is a mass percent or a volume percent value. See <a class="reference internal" href="#customgas.Percent" title="customgas.Percent"><code class="xref py py-func docutils literal notranslate"><span class="pre">Percent()</span></code></a>.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>kwargs</strong> – name: str | gas_mix: dict  percent: int</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p><cite>Gas</cite> instance</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="customgas.Gas.update_state">
<span class="sig-name descname"><span class="pre">update_state</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.Gas.update_state" title="Link to this definition"></a></dt>
<dd><p>Set a new gas-state in order to the <cite>input_pair</cite>. Be carful to
use the values in the right order. See
<a class="reference external" href="https://coolprop.org/_static/doxygen/html/namespace_cool_prop.html#a58e7d98861406dedb48e07f551a61efb">CoolProp-Documentation</a></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>args</strong> – list [int | float]</p>
</dd>
</dl>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="customgas.Percent">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">customgas.</span></span><span class="sig-name descname"><span class="pre">Percent</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.Percent" title="Link to this definition"></a></dt>
<dd><p>An Enum class to use the percent in mass- or volumepercent.</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="customgas.InputPairs">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">customgas.</span></span><span class="sig-name descname"><span class="pre">InputPairs</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#customgas.InputPairs" title="Link to this definition"></a></dt>
<dd><p>An Enum-class to use one of the input-pairs.</p>
<p>Pressure and Temperature or Temperature and density</p>
</dd></dl>

</section>

  <hr/>

  <div role="contentinfo">
    <p>&#169; Copyright 2026, Dennis Straub.</p>
  </div>
