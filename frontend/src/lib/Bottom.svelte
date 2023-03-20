<script>
    import { A, P } from 'flowbite-svelte';
</script>

<footer class="py-10 border-t border-gray-200">
    <div class="px-2 sm:px-4">
        <div class="mx-auto flex flex-col container">
            <div class="flex flex-row gap-14 mb-10 justify-center">
                <div class="flex flex-col">
                    <P class="mb-3"><span class="font-bold text-sm">READRetro was brought to you by:</span></P>
                    <A class="flex-grow" href="https://sites.google.com/view/kimlab" target="_blank"><img class="w-52" src="/ecolab.png" alt="Laboratory for Ecology at Korea Advanced Institute for Science & Technology" /></A>
                </div>
                <div class="flex flex-col">
                    <P class="mb-3"><span class="font-bold text-sm">Website was designed &amp; developed by:</span></P>
                    <A class="flex-grow" href="https://pnucolab.com" target="_blank"><img class="w-72" src="/pnucolab.png" alt="Computational Omics Laboratory at Pusan National University" /></A>
                </div>
            </div>
            <P class="text-center">© 2023 <A href="https://sites.google.com/view/kimlab" target="_blank">Laboratory for Ecology</A> and <A href="https://pnucolab.com" target="_blank">Computational Omics Laboratory</A>, all rights reserved.</P>
        </div>
    </div>
</footer>
