import json
from openai import OpenAI

# Load your input JSON file
with open("sweet_term_typing_test_data.json", "r", encoding="utf-8") as infile:
    terms_data = json.load(infile)

# Initialize OpenAI client
client = OpenAI(
    base_url="#",
    api_key="#",
)

# Shared prompt prefix (static portion)
prompt_prefix = """
From the sample terms provided for each type, identify the type(s) of the term in [VAR]. A term can have more than one type. Only write the types in quotation marks, and if there is more than one, separate them with a comma. The types must be selected from the given list—no more, no less.

Type: hydrocarbon
Term: c12h8
Term: c12h10

Type: role
Term: pre existing
Term: secure

Type: spectral band
Term: yellow
Term: fm

Type: trust
Term: defended
Term: observed

Type: saffir simpson scale
Term: category3
Term: category5

Type: organic compound
Term: ch3cn
Term: ch2o2

Type: system state
Term: balance
Term: exogenous

Type: Instant
Term: 40.4mya
Term: 4000mya

Type: provenance role
Term: author
Term: creator

Type: age
Term: ludfordian
Term: homerian

Type: temperature range
Term: N595ed4dab6ca4556b7c7f9233e5c24a7
Term: Nf180d0d7969b41f3a07b2d736ace205b

Type: energy flux wm2
Term: N25f25f9f64774c09a2aac945739543bb
Term: N36cedbb3d3234c43ba70fcb6f4ef2e3a

Type: dimensionless ratio
Term: specific storage
Term: richardson number

Type: element
Term: mo
Term: selenium

Type: unit defined by product
Term: meter cubed per kelvin
Term: kelvin per meter

Type: consumer
Term: tertiary consumer
Term: secondary consumer

Type: inorganic acid
Term: nitric acid
Term: nitric acid trihydrate

Type: chemical state
Term: non polar
Term: radioactive

Type: biological role
Term: macronutrient
Term: carcinogen

Type: activity level
Term: inactive
Term: extinct

Type: physical state
Term: ionized state
Term: burned

Type: x class
Term: x36 class
Term: x38 class

Type: distance
Term: remote
Term: close

Type: connectivity
Term: semiconfined
Term: unconnected

Type: horizontal coordinate system
Term: mercator
Term: oblique mercator

Type: unit derived by raising to power
Term: per kelvin
Term: per mole

Type: earth western boundary current
Term: kurishio current
Term: agulhas current

Type: impact
Term: major
Term: minimal

Type: spatial scale
Term: regional
Term: planetary scale

Type: beaufort scale
Term: beaufort4
Term: beaufort0

Type: Organization
Term: N678483a45e6e4819bab6f0471ea8dafe

Type: isotope
Term: th229
Term: o17

Type: inorganic compound
Term: dichlorine peroxide
Term: hypochlorous monoxide

Type: unit derived by shifting
Term: degree f
Term: degree c

Type: period
Term: statherian
Term: ectasian

Type: ion
Term: nitrate
Term: bicarbonite

Type: unit derived by scaling
Term: mhz
Term: gigahertz

Type: epoch
Term: wenlock
Term: furongian

Type: reference frame
Term: heliocentric
Term: barycentric

Type: radioactive substance
Term: u239
Term: al26

Type: temperature gradient range
Term: positive slope
Term: negative slope

Type: geospatial interface protocol
Term: wcs
Term: web map server

Type: height range km
Term: N8e33dbe0393249b08c96a0cf30e84987
Term: Nc63c018ab60d486ab1d997ce97c10659

Type: chemical role
Term: outgas
Term: dilute

Type: size
Term: microscopic
Term: medium

Type: wave state
Term: eddy
Term: destructive

Type: duration
Term: 3month
Term: 1month

Type: allotrope
Term: cl2
Term: c6

Type: spatial configuration
Term: descending
Term: asymmetric

Type: noble gas
Term: he
Term: ar

Type: great circle
Term: terminator
Term: geostationary

Type: speed state
Term: rapid
Term: quiescent

Type: equilibrium state
Term: isochoric
Term: isostatic

Type: dry winter climate
Term: dwc
Term: dwa

Type: season
Term: summer
Term: spring

Type: halon
Term: cbrf2
Term: cbrf3

Type: horizontal direction
Term: westward
Term: leeward

Type: shape
Term: oblate
Term: rounded

Type: moisture state
Term: hydrophilic
Term: deiced

Type: angular extent
Term: full disk

Type: m class
Term: m3 class
Term: m9 class

Type: a class
Term: a9 class
Term: a2 class

Type: hydrogeological property
Term: retardation factor

Type: earth eastern boundary current
Term: peru current
Term: canary current

Type: biological state
Term: nutrient rich
Term: assimilated

Type: actinoid
Term: u
Term: th

Type: solid state
Term: pitted
Term: crystalline

Type: frequency
Term: interrupted
Term: cyclic

Type: north latitude band
Term: N9943f07275c849cd85a00984c3eebcf1
Term: N3b2f04610fec4d8d8982203abbde756c

Type: substance form
Term: fragment
Term: particle

Type: transition metal
Term: ch
Term: zi

Type: component
Term: internal
Term: ambient

Type: halogen
Term: cl
Term: br

Type: c class
Term: c4 class
Term: c3 class

Type: thermodynamic state
Term: maximum entropy
Term: local thermodynamic equilibrium

Type: wavelength band nm
Term: N3a0d5a4b98734bbb9344b3b8344ad0de
Term: Nc56eb887b2db47f7be3dee2b12d41e65

Type: representative role
Term: defining
Term: actual

Type: enhanced fujita scale
Term: ef4
Term: ef2

Type: vertical coordinate
Term: sigma naught
Term: elevation

Type: latitude line
Term: N11d4ea91c0d0421290c5e90d5c915444
Term: pole

Type: latitude band
Term: high latitude
Term: subtropical

Type: cfc
Term: cfc113
Term: ccl2f2

Type: c
Term: csb
Term: cwa

Type: spectral line
Term: ni6768
Term: lyman alpha

Type: era
Term: neoarchean
Term: mesozoic

Type: angular direction
Term: counterclockwise
Term: retrograde

Type: solstice
Term: december solstice
Term: summer solstice

Type: environmental standards body
Term: fish and wildlife service
Term: fws

Type: south latitude line
Term: N0cb71d834be045ef9595a6701d405e08

Type: angular coordinate
Term: right ascension
Term: roll

Type: d
Term: dwc
Term: dwa

Type: direction
Term: left
Term: transverse

Type: north latitude line
Term: N60a6164ace3942469c272b1b7e90e44b

Type: magnetic pole
Term: south magnetic pole
Term: north magnetic pole

Type: b
Term: bw
Term: hot low latitude steppe climate

Type: fluid equilibrium state
Term: hydrostatic
Term: nonhydrostatic

Type: vertical direction
Term: downward
Term: up

Type: precipitation range
Term: N142d07f345ca48658230d403bd01a5df
Term: N308480a0c7e445998c614c8d92310c70

Type: vertical extent
Term: high
Term: shallow

Type: chlorophyll
Term: pheophytin
Term: chlorophyll a

Type: wavelength nm
Term: N81fa88f053d04b0c98c84284aed9ee99
Term: Na4d3d9e6a9184236ab1ca70e6ebe17a0

Type: frequency band mhz
Term: N0c680e6b70e841078cb9ebbc2e025412
Term: Ne870f4c6529640b0916c6d058982d2d2

Type: visibility
Term: bright
Term: transparent

Type: retrieval approach
Term: active

Type: geosphere
Term: earth geosphere

Type: base unit
Term: second
Term: ratio

Type: self describing format
Term: hdf5
Term: hdf

Type: lithosphere
Term: earth lithosphere

Type: b class
Term: b2 class
Term: b5 class

Type: photic zone
Term: earth photic zone

Type: prefix
Term: centi
Term: hecto

Type: interface protocol
Term: opendap
Term: dods

Type: equinox
Term: spring equinox
Term: autumnal equinox

Type: fluid state
Term: laminar
Term: rareified

Type: qualifier
Term: middle
Term: medium

Type: bathypelagic zone
Term: earth bathypelagic zone

Type: format
Term: grib
Term: binary

Type: state of matter
Term: solid
Term: gaseous

Type: polar coordinates
Term: polar stereographic

Type: earth ocean
Term: southern ocean
Term: caribbean sea

Type: chalcogen
Term: se

Type: alkene
Term: c2h4
Term: c3h6

Type: ocean area
Term: pt1million_km2
Term: pt4million_km2

Type: orbital configuration
Term: eclipse
Term: conjunction

Type: realm configuration
Term: aloft
Term: spaceborne

Type: byte order
Term: middle endian
Term: little endian

Type: rain state
Term: scattered
Term: severe

Type: crust
Term: earth crust

Type: eon
Term: phanerozoic
Term: hadean

Type: biochemical state
Term: hypoxic
Term: anerobic

Type: mineral assessment
Term: paramarginal

Type: unit
Term: formazin turbidity unit
Term: ftu

Type: alkali metal
Term: k
Term: na

Type: alkane
Term: c4h10
Term: ch4

Type: a
Term: am
Term: tropical monsoon climate

Type: alkaline earth metal
Term: ca
Term: be

Type: mesosphere
Term: earth mesosphere

Type: depth range km
Term: N1bac926d0ef34085a8f35505895d7636
Term: Nb2bb4b1402f744f09137d4466d2bab10

Type: geomagnetic field
Term: international geomagnetic reference field

Type: spatial source
Term: non point
Term: mobile

Type: logarithmic unit
Term: db

Type: wavelength cm
Term: Nff4f3021688648d787dda60b01ebd6ee

Type: south latitude band
Term: N5c61f506080d4749a31298b6ccb81b6c
Term: N3c3adc587bf243049967a7859ed53a37

Type: nonmetal
Term: c

Type: fujita pearson scale
Term: f4
Term: f5

Type: compression method
Term: z

Type: environmental law
Term: endangered species act
Term: federal clean air act

Type: planet
Term: earth

Type: land use
Term: commercial
Term: populated

Type: classifier
Term: neural network
Term: naive bayes

Type: precipitation range cm
Term: Nbff8158e4df444319aca9a6008fcf401

Type: conduction role
Term: insulator

Type: month range
Term: N00cd20fd831f482894ad2b98aa3193ba
Term: N42774f8ab23a43729b426d79c8c07b21

Type: ocean gyre
Term: indian ocean gyre
Term: south atlantic gyre

Type: hcfc
Term: hcfc142b
Term: hcfc140a

Type: federal governing body
Term: faa

Type: difference
Term: ndvi
Term: normalized difference vegetation index

Type: size range micron
Term: Nf911b89c728746dbaa21db960509f9e3
Term: N6414eb5578a5429a90cfa416e85e4980

Type: distance range km
Term: earth atmosphere synoptic scale

Type: wet summer dry winter climate
Term: csb
Term: cwa

Type: binary state
Term: live
Term: nonliving

Type: ocean volume
Term: pt6million_km3
Term: pt0million_km3

Type: environmental standard
Term: neshap
Term: national emission standards for hazardous air pollutant

Type: e
Term: polar marine climate
Term: em

Type: metalloid
Term: b
Term: si

Type: radiation medium interaction quantity
Term: angstrom exponent

Type: spatial reference system
Term: tait bryan angle
Term: astronomical

Type: earth ocean current
Term: deep ocean current
Term: benguela current

Type: electromagnetic quantity
Term: plasma parameter

Type: peroxide
Term: cl2o2
Term: hno4

Type: interval
Term: normalized range

Type: physical constant
Term: solar constant

Type: horizontal coordinate
Term: colatitude
Term: x

Type: producer
Term: primary producer

Type: abyssopelagic zone
Term: abyssopelagic zone

Type: post transition metal
Term: pb

Type: time zone
Term: ut
Term: universal time

Type: habitat
Term: nursery
Term: feeding habitat

Type: e layer
Term: earth e layer

Type: interpolation method
Term: distance weighting

Type: potential evapotranspiration
Term: annual potential evapotranspiration

Type: physical role
Term: antifreeze
Term: cryoprotectant

Type: core
Term: earth core

Type: consistence property
Term: void ratio

Type: f layer
Term: earth f layer

Type: stratosphere
Term: earth stratosphere

Type: time frame
Term: synodic

Type: upper mantle
Term: earth upper mantle

Type: exosphere
Term: earth exosphere

Type: fluid property
Term: drag coefficient

Type: half potential evapotranspiration
Term: annual half potential evapotranspiration

Type: atmosphere
Term: earth atmosphere

Type: d layer
Term: earth d layer


"""

output_data = []

# Loop over each term in the input file
for entry in terms_data:
    term_id = entry["id"]
    term_text = entry["term"]

    # Prepare full prompt with term injected into [VAR]
    full_prompt = f"{prompt_prefix}\n[VAR]{term_text}[VAR]"

    try:
        # Get completion from model
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )

        # Parse the types from model response
        types_raw = response.choices[0].message.content.strip()
        types_list = [t.strip().strip('"') for t in types_raw.split(",") if t.strip()]

        # Create structured output
        output_data.append({
            "id": term_id,
            "types": types_list
        })

    except Exception as e:
        print(f"Error processing term {term_text}: {e}")

# Write output to JSON file
with open("output_deepseek.json", "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=2)

print("Done. Output written to output.json.")
