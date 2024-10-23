document.addEventListener('alpine:init', () => {
    Alpine.data('formHandler', () => ({
        fecha: new Date().toLocaleDateString(),
        selectedType: 'josh',
        items: [
            {
                id: 1,
                cantidad: '',
                unidad: '',
                descripcion: ''
            }
        ],

        addItem() {
            this.items.push({
                id: Date.now(),
                cantidad: '',
                unidad: '',
                descripcion: ''
            });
        },

        removeItem(index) {
            if (this.items.length > 1) {
                this.items.splice(index, 1);
            }
        },

        async submitForm(e) {
            const formData = {
                fecha: this.fecha,
                tipo: this.selectedType,
                nombre_proveedor: e.target.nombre_proveedor.value,
                nit: e.target.nit.value,
                firma: e.target.firma.value,
                items: this.items
            };

            try {
                const response = await fetch('/generar-pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `solicitud_${new Date().toISOString().slice(0,10)}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    a.remove();
                } else {
                    throw new Error('Error al generar el PDF');
                }
            } catch (error) {
                alert('Error al generar el PDF: ' + error.message);
            }
        }
    }));
});