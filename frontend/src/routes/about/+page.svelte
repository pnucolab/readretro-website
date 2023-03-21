<script>
    import { Heading, P } from 'flowbite-svelte';
</script>

<Heading tag="h2" class="mt-5 mb-2">About</Heading>
<Heading tag="h5" class="font-light mb-10">Retrosynthesis, READRetro, and the READRetro Website</Heading>

<Heading tag="h5" class="mt-5 mb-2">Retrosynthesis</Heading>
<P>Retrosynthesis is a problem-solving technique used in organic chemistry to design a synthetic route for a target molecule. It involves breaking down the target molecule into simpler starting materials, which are then sequentially converted into the desired product through a series of chemical reactions.</P>
<P>The goal of retrosynthesis is to identify the most efficient and practical route to synthesize a target molecule. To do this, chemists use a variety of strategies and techniques, such as functional group interconversions, protecting group chemistry, and stereoselective reactions.</P>
<P>The retrosynthetic analysis begins with the identification of functional groups and other structural features that are likely to be preserved during the synthesis. These key functional groups are then used to guide the disconnection of the target molecule into smaller fragments. This process is repeated until the fragments can be obtained from commercially available starting materials or from known synthetic procedures.</P>
<P>Once the retrosynthetic analysis is complete, the chemist can then plan the forward synthesis by selecting appropriate reactions and reagents to connect the fragments in a stepwise manner, eventually arriving at the target molecule.</P>

<Heading tag="h5" class="mt-5 mb-2">READRetro</Heading>
<P>Elucidating the biosynthetic pathways of natural products has been a major focus of biochemistry and pharmacy, but predicting the whole pathways from target molecules to metabolic building
   blocks has remained a challenge. Here we introduce READRetro, a practical bio-retrosynthesis tool for planning the biosynthetic pathways of natural products. READRetro effectively resolved
   the trade-off between generalizability and memorability in bio-retrosynthesis by having two separate modules each responsible for each ability.</P>
<P>Specifically, READRetro utilized a rule-based retriever for memorability and an ensemble of two dual representation-based deep learning models for generalizability.
    Through extensive experiments, READRetro was demonstrated to outperform existing models by a large margin in both generalizability and memorability. READRetro was also capable of predicting
    the known pathways of complex plant secondary metabolites such as monoterpene indole alkaloids, demonstrating its applicability to real-world bio-retrosynthesis planning of natural products.
    The website (https://www.readretro.net) and open-source code are provided for using READRetro as a practical tool with state-of-the-art performance for natural product biosynthesis research.</P>

<Heading tag="h5" class="mt-5 mb-2">READRetro Website</Heading>
<P>READRtro was developed as a a web tool designed to assist chemists and researchers in tackling the complex problem of retrosynthesis with ease and efficiency.
   The platform is powered by cutting-edge technologies such as SvelteKit, FastAPI, Celery, PostgreSQL, and Redis, providing a powerful and scalable
   infrastructure to support your synthetic chemistry endeavors.</P>
<P>The front-end is built on the SvelteKit framework, providing a highly optimized and responsive user interface that enables retrosynthesis tasks to be submitted
   and executed easily and efficiently.</P>
<P>The back-end is powered by FastAPI, a modern web framework designed for high-performance applications. With FastAPI, you can enjoy lightning-fast response
   times and robust functionality, ensuring that your submitted tasks are executed quickly and efficiently.</P>
<P>Celery is utilized as a powerful and scalable solution for task queue management. Redis and PostgreSQL are used as the backend for Celery,
   providing a highly efficient and performant solution for managing and storing your submitted retrosynthesis tasks.</P>
<P>The whole website is packaged using Docker, a containerization platform that enables easy deployment and management of
   applications across a wide range of environments.</P>