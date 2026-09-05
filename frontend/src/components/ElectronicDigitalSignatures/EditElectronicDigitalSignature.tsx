import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient ,useQuery} from "@tanstack/react-query"
import { Pencil } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import {
  type ElectronicDigitalSignaturePublic,
  ElectronicDigitalSignaturesService,
  OrganizationsService,
  SignatureTypesService,
  EmployeesService,
  CertificationCentersService,
} from "@/client"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DropdownMenuItem } from "@/components/ui/dropdown-menu"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const formSchema = z.object({
  date_certificate: z.iso.datetime({
    message: "Must be a valid ISO datetime string",
  }),
  date_container: z.iso.datetime({
    message: "Must be a valid ISO datetime string",
  }),
  organization_id: z.uuid({ message: "Organization is required" }),
  signature_type_id: z.uuid({ message: "Signature type is required" }),
  employee_id: z.uuid({ message: "Employee is required" }),
  certification_center_id: z.uuid({
    message: "Certification Center is required",
  }),
})

type FormData = z.infer<typeof formSchema>

interface EditElectronicDigitalSignatureProps {
  electronicDigitalSignature: ElectronicDigitalSignaturePublic
  onSuccess: () => void
}

const EditElectronicDigitalSignature = ({
  electronicDigitalSignature,
  onSuccess,
}: EditElectronicDigitalSignatureProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const { data: organizationsData, isLoading: isLoadingOrganizations } =
    useQuery({
      queryFn: async () => {
        const response = await OrganizationsService.readOrganizations({
          query: { skip: 0, limit: 100 },
        });
        return response.data; // или response, в зависимости от вашего API
      },
      queryKey: ["organizations"],
    });
  const organizations = organizationsData?.data || [];

  const { data: signatureTypesData, isLoading: isLoadingSignatureTypes } =
    useQuery({
      queryFn: async () => {
        const response = await SignatureTypesService.typesReadSignatureTypes({
          query: { skip: 0, limit: 100 },
        });
        return response.data; // или response, в зависимости от вашего API
      },
      queryKey: ["signature-types"],
    });
  const signatureTypes = signatureTypesData?.data || [];

  const { data: employeesData, isLoading: isLoadingEmployees } = useQuery({
    queryFn: async () => {
      const response = await EmployeesService.readEmployees({
        query: { skip: 0, limit: 100 },
      });
      return response.data; // или response, в зависимости от вашего API
    },
    queryKey: ["employees"],
  });
  const employees = employeesData?.data || [];

  const {
    data: certificationCentersData,
    isLoading: isLoadingCertificationCenters,
  } = useQuery({
    queryFn: async () => {
      const response =
        await CertificationCentersService.centersReadCertificationCenters({
          query: { skip: 0, limit: 100 },
        });
      return response.data; // или response, в зависимости от вашего API
    },
    queryKey: ["certification-centers"],
  });
  const certificationCenters = certificationCentersData?.data || [];


  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      date_certificate: electronicDigitalSignature?.date_certificate,
      date_container: electronicDigitalSignature?.date_container,
      organization_id: electronicDigitalSignature?.organization.id,
      signature_type_id: electronicDigitalSignature?.signature_type.id,
      employee_id: electronicDigitalSignature?.employee.id,
      certification_center_id: electronicDigitalSignature?.certification_center.id,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) =>
      ElectronicDigitalSignaturesService.digitalSignaturesUpdateElectronicDigitalSignature(
        {
          path: { id: electronicDigitalSignature.id },
          body: data,
        },
      ),
    onSuccess: () => {
      showSuccessToast("Electronic Digital Signature updated successfully")
      setIsOpen(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ["electronic-digital-signatures"],
      })
    },
  })

  const onSubmit = (data: FormData) => {
    mutation.mutate(data)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => setIsOpen(true)}
      >
        <Pencil />
        Edit ElectronicDigitalSignature
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-md">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <DialogHeader>
              <DialogTitle>Edit Electronic Digital Signature</DialogTitle>
              <DialogDescription>
                Update the Electronic Digital Signature details below.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <FormField
                control={form.control}
                name="date_certificate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Date Certificate{" "}
                      <span className="text-destructive">*</span>
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Date Certificate"
                        type="datetime-local"
                        {...field}
                        required
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="date_container"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Date Container <span className="text-destructive">*</span>
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Date Container"
                        type="datetime-local"
                        {...field}
                        required
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="organization_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Organization <span className="text-destructive">*</span>
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isLoadingOrganizations}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select organization" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {organizations.map((org) => (
                          <SelectItem key={org.id} value={org.id}>
                            {org.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="signature_type_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Signature type <span className="text-destructive">*</span>
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isLoadingSignatureTypes}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select signature type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {signatureTypes.map((signatureType) => (
                          <SelectItem
                            key={signatureType.id}
                            value={signatureType.id}
                          >
                            {signatureType.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="employee_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Employee <span className="text-destructive">*</span>
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isLoadingEmployees}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Employee" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {employees.map((employee) => (
                          <SelectItem key={employee.id} value={employee.id}>
                            {employee.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="certification_center_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Certification Center{" "}
                      <span className="text-destructive">*</span>
                    </FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isLoadingCertificationCenters}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Certification Center" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {certificationCenters.map((certificationCenter) => (
                          <SelectItem
                            key={certificationCenter.id}
                            value={certificationCenter.id}
                          >
                            {certificationCenter.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline" disabled={mutation.isPending}>
                  Cancel
                </Button>
              </DialogClose>
              <LoadingButton type="submit" loading={mutation.isPending}>
                Save
              </LoadingButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default EditElectronicDigitalSignature
